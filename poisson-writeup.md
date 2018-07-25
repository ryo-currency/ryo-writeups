# Stopping Verge-like offline timestamp attacks with Poisson probability check

**FOSS snippet included. Please use the code in the snippet. RYO code is copyrighted.**

If you would like to invest in one of very few cryptonote currencies that does actual development, have a look at our website [ryo-currency.com](https://ryo-currency.com)

<p align="center"><img src="https://ryo-currency.com/img/svg/ryo-privacy-for-everyone.svg" width="300"></p>

### Foreword
51% attacks stopped being a mere threoretical possibility and started to be a practical concern for smaller coins. While they can never be mitigated completely, the easiest and most lucrative avenue of attack is to strike at the rate-control algorithm using forged timestamps to print thousands of blocks very fast. To prevent this most nodes will not accept blocks that are more that a few minutes in the future (a.k.a Future Time Limit or FTL). In this article I will explain how to bypass FTL and how to mitigate that bypass.

### How to bypass FTL check
1. Disable the FTL check on your local node
2. Cut all connections to the network.
3. Set the timestamp ahead X hours.
4. Do whatever is needed to cheat the rate control algorithm. For Sumokoin algo that was alternating timestamps in 2-1 pattern.
5. After X hours passed, you can online your node and let the others reorg to you.

### How to stop that attack
We can put a second layer of protection here on step 5. The critical issue is that the attacker needs our nodes to reorg to him. We can ask a question - **"How likely is it that someone came up with 10,000 blocks in 5 hours, assuming that the rate control algorithm did not fail?"**.

While you are probably screaming "That assumption is wrong! It did fail!", those more scientifically inclined will recognise that **assuming that the rate control algorithm did not fail** is something we call a [null hypothesis](https://en.wikipedia.org/wiki/Null_hypothesis) in statistics. Computers are not as smart as you and therefore we need to set out the question formally and dress it in something they understand (numbers).

### Prussian army to the rescue!
In the late 19th century statisticians started to collate various data, for you guessed it ~~Facebook~~, I mean insurance companies. One very clever fellow ([Bortkiewicz](https://en.wikipedia.org/wiki/Ladislaus_Bortkiewicz)) noticed that the plot of deaths in Prussian cavalry corps looks exactly like the plot of child suicides. What do those two have in common? The correct answer is exactly nothing.

One fairly complicated equation later we are ready to calculate the probablity of unrelated events with a fixed probability. This is of course our block finding probability.

![Poisson formula](https://wikimedia.org/api/rest_v1/media/math/render/svg/df3b6a7648b33ca3a987b970e4e8a719f888edb5)

### What does it mean?

This allows us to to say that the chance of someone honestly coming up with 10000 blocks in 5 hours is so small that it won't happen in the projected life of the universe. As such when we do see it, it means that someone bypassed the rate control algorithm and we can reject that reorg.

```
// MIT License

// Copyright (c) 2018 ryo-currency

// Permission is hereby granted, free of charge, to any person obtaining a copy
// of this software and associated documentation files (the "Software"), to deal
// in the Software without restriction, including without limitation the rights
// to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
// copies of the Software, and to permit persons to whom the Software is
// furnished to do so, subject to the following conditions:

// The above copyright notice and this permission notice shall be included in all
// copies or substantial portions of the Software.

// THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
// IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
// FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
// AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
// LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
// OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
// SOFTWARE.

struct common_config
{
	static constexpr uint64_t POISSON_CHECK_TRIGGER = 10;  // Reorg size that triggers poisson timestamp check
	static constexpr uint64_t POISSON_CHECK_DEPTH = 60;   // Main-chain depth of the poisson check. The attacker will have to tamper 50% of those blocks
	static constexpr double POISSON_LOG_P_REJECT = -75.0; // Reject reorg if the probablity that the timestamps are genuine is below e^x, -75 = 10^-33
}

// Calculate ln(p) of Poisson distribution
// Original idea : https://stackoverflow.com/questions/30156803/implementing-poisson-distribution-in-c
// Using logarithms avoids dealing with very large (k!) and very small (p < 10^-44) numbers
// lam     - lambda parameter - in our case, how many blocks, on average, you would expect to see in the interval
// k       - k parameter - in our case, how many blocks we have actually seen
//           !!! k must not be zero
// return  - ln(p)

double calc_poisson_ln(double lam, uint64_t k)
{
	double logx = -lam + k * log(lam);
	do
	{
		logx -= log(k); // This can be tabulated
	} while(--k > 0);
	return logx;
}

//------------------------------------------------------------------
// This function attempts to switch to an alternate chain, returning
// boolean based on success therein.
bool Blockchain::switch_to_alternative_blockchain(std::list<blocks_ext_by_hash::iterator> &alt_chain, bool discard_disconnected_chain)
{

[...]

	// For longer reorgs, check if the timestamps are probable - if they aren't the diff algo has failed
	// This check is meant to detect an offline bypass of timestamp < time() + ftl check
	// It doesn't need to be very strict as it synergises with the median check
	if(alt_chain.size() >= common_config::POISSON_CHECK_TRIGGER)
	{
		uint64_t alt_chain_size = alt_chain.size();
		uint64_t high_timestamp = alt_chain.back()->second.bl.timestamp;
		crypto::hash low_block = alt_chain.front()->second.bl.prev_id;

		//Make sure that the high_timestamp is really highest
		for(const blocks_ext_by_hash::iterator &it : alt_chain)
		{
			if(high_timestamp < it->second.bl.timestamp)
				high_timestamp = it->second.bl.timestamp;
		}

		uint64_t block_ftl = check_hard_fork_feature(FORK_V3_DIFFICULTY) ? common_config::BLOCK_FUTURE_TIME_LIMIT_V3 : common_config::BLOCK_FUTURE_TIME_LIMIT_V2;
		// This would fail later anyway
		if(high_timestamp > get_adjusted_time() + block_ftl)
		{
			LOG_ERROR("Attempting to move to an alternate chain, but it failed FTL check! timestamp: " << high_timestamp << " limit: " << get_adjusted_time() + block_ftl);
			return false;
		}

		LOG_PRINT_L1("Poisson check triggered by reorg size of " << alt_chain_size);

		uint64_t failed_checks = 0, i = 1;
		constexpr crypto::hash zero_hash = {{0}};
		for(; i <= common_config::POISSON_CHECK_DEPTH; i++)
		{
			// This means we reached the genesis block
			if(low_block == zero_hash)
				break;

			block_header bhd = m_db->get_block_header(low_block);
			uint64_t low_timestamp = bhd.timestamp;
			low_block = bhd.prev_id;

			if(low_timestamp >= high_timestamp)
			{
				LOG_PRINT_L1("Skipping check at depth " << i << " due to tampered timestamp on main chain.");
				failed_checks++;
				continue;
			}

			double lam = double(high_timestamp - low_timestamp) / double(common_config::DIFFICULTY_TARGET);
			if(calc_poisson_ln(lam, alt_chain_size + i) < common_config::POISSON_LOG_P_REJECT)
			{
				LOG_PRINT_L1("Poisson check at depth " << i << " failed! delta_t: " << (high_timestamp - low_timestamp) << " size: " << alt_chain_size + i);
				failed_checks++;
			}
		}

		i--; //Convert to number of checks
		LOG_PRINT_L1("Poisson check result " << failed_checks << " fails out of " << i);

		if(failed_checks > i / 2)
		{
			LOG_ERROR("Attempting to move to an alternate chain, but it failed Poisson check! " << failed_checks << " fails out of " << i << " alt_chain_size: " << alt_chain_size);
			return false;
		}
	}

[...]
}
```
