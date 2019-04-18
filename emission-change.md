# Ryo Emission Change Discussion

**Published April 18th, 2019**

## Preface

Changing the emission curve is a serious consideration for any cryptocurrency. Some people consider that the emission should never change once a coin is launched, and that it is a part of the social contract created at the genesis block. Over the last year, the Ryo team has heard from many community members that the current emission schedule inherited from Sumokoin is ill-fitted for both short and long term users of the coin and that Ryo's emission should be based on a rational community debate instead of automatically inherited from Sumokoin. This proposal was created as a collaboration between key community and core team members.

Sumokoin initially implemented the “camel-emission” curve which has the positive benefit of not emitting the majority of coins within the first few years before adoption, and instead is modeled after real world mining operations. The base reward starts at 32 coins per block, increases to 97.92 coins per block in 2021, before decreasing to the tail emission of 4 coins per block in 2033.

This emission gives miners time to find the project and mine coins before the block reward drops too quickly. However, the chosen emission curve is at the cost of excessively high inflation over the next couple years due to the peak reward being over three times the initial block reward. Conversely, having too fast of an emission and too rapid decrease in block reward benefits only the early miners of the coin who mine it before it becomes popular.

## How can emission be modified?

Currently, there are five more block reward increases over the next 2.5 years for a max block reward of 97.92 coins per block to be reached. This proposed model changes it so there are only two more block reward increases for a max block reward of 65.07 Ryo per block over the next 12 months. After this new peak, the block reward will start decreasing and reach tail emission in the year 2041.

The change is done by modifying only two parameters of the original curve. First, peak emission will be brought forward to 2.5–3 years after launch of the coin, instead of 4–4.5 years after launch. Secondly, emission speed factor will be increased from 19 to 20 on the decline portion of the curve.

Total supply will still be approximately 88 Million coins, but that number will not be reached until 2048, or about 10 years later than current schedule.

The proposed change would take effect in a little over a year from the day this document was published. Care was taken in order to make any change in emission not too sudden to allow for adequate time for investors and miners to adjust to the proposed changes.

## Block reward in detail

![Block reward chart](emission-change-assets/chart-block-reward.png?raw=true "Block reward chart")

The above graph shows the current block reward schedule (blue) vs the proposed change (green) over 20 years. Currently, the block reward is at 48.59 Ryo per block. The next two increases will be identical to the current schedule, however after those next two increases the curve will start to decrease. The highest block reward will end up at 65.07 instead of  97.92 Ryo per block as currently scheduled.

In order to keep the same max supply before tail emission, the block reward will decrease more slowly after the peak compared to the original model. Around the year 2026, the block reward will be higher than it would have been with the current schedule.

The block reward in this proposed model is not scheduled to change from the current path for one year from the next reward increase. This amount of time is chosen in order to let miners who may not have been planning on mining Ryo until the peak a fair chance to prepare for the emission change.

## Inflation percentage in detail

![Inflation chart](emission-change-assets/chart-inflation.png?raw=true "Inflation chart")

This graph shows the annual inflation by year. In both models, inflation will be 80% over the next year since this proposal will not change emission until April 2020, after which the proposed model will have a significant reduction in inflation for several years.

Since block reward will decrease towards tail emission more slowly in the proposed model, inflation will be slightly higher in year 2024 and beyond, however this is not seen as a negative.

## Emission percentage in detail

![Emission chart](emission-change-assets/chart-emission.png?raw=true "Emission chart")

With the current model, Ryo will be 99% mined by the year 2036. With the proposed model, 99% emission will be reached in 2048. The proposed emission curve is very similar to Bitcoin’s emission curve. See charts at the bottom of this document for comparison to both Monero and Bitcoin.

## Does this affect the development fund?

![Development fund chart](emission-change-assets/chart-development-fund.png?raw=true "[Development fund chart")

This proposed model will not change the amount of coins or frequency of the Ryo dev fund. Since emission will be slowed down, it will however at times make the dev fund be a greater percentage of circulating supply.

The original Sumokoin premine was 8.8 Million coins. With their premine unlock schedule, the Sumokoin dev fund will be worth 30% of their coin’s circulating supply next year.

The Ryo dev fund burned 8.7M of those coins from the supply, and re-introduced 8 Million coins emitted over six years. With the current model, the dev fund reaches a maximum of 12% of circulating supply.

With the proposed emission model, the Ryo dev fund remains at 8M coins emitted over the same six years, and will reach a maximum of 15% of circulating supply in the year 2024 and decrease from there.

In both the current and proposed model, the Ryo dev fund will end up as 9% of total supply at tail emission.

## How does this compare to Bitcoin or Monero?

### Block reward

![Block reward chart](emission-change-assets/chart-block-reward-with-bitcoin-monero.png?raw=true "Block reward chart")

This chart shows a comparison of the block reward curves for Ryo, Bitcoin, and Monero. Note that each coin has different block times which affect how many coins are emitted per minute. The jump in Monero's curve at year three is when they switched from one minute to two minute block times.

### Inflation

![Inflation chart](emission-change-assets/chart-inflation-with-bitcoin-monero.png?raw=true "Inflation chart")

This chart shows inflation per year of Ryo, Bitcoin, and Monero. Inflation is calculated at twelve month intervals from the coin's genesis block. Monero shows low visible inflation because of its steep emission curve in year one. Inflation is not shown for the first year since it is infinite.

### Emission

![Emission chart](emission-change-assets/chart-emission-with-bitcoin-monero.png?raw=true "Emission chart")

This chart shows the emission curve of Ryo, Bitcoin, and Monero. The proposed change would make it so that half of all Ryo are mined by the year 2023, or six years after the launch of the coin. Bitcoin emitted half of its supply four years after launch, and Monero only 16 months after launch. [Source](https://docs.google.com/spreadsheets/d/1qXi7zUSIh7F6UuSuhOryyFbHEy_LJuym3I3neAga_2s/edit#gid=239466694)

## Conclusion

This proposed model was created after the topic of an emission change has been brought up several times over the past year since the Sumokoin and Ryo chains diverged. The specifics of this model are accomplished by only changing 3–4 lines of code in the current emission function. Specifically, the peak reward block height, and the emission speed factor after the peak height.

The purpose of this proposal is to gather feedback on the fundamentals of changing emission in general, and if this proposed model accomplishes improving the monetary policy of Ryo. Since any immediate changes might be seen as negative, this model would take effect at block height 394470, which is approximately 13.5 months from the date of this document. Avoiding a sudden change in emission should allow both current and new supporters of the coin to adapt to the changes, if accepted by the community. It is important to consider any changes to the emission curve carefully, as monetary policy changes are not something that should be frequently modified.

These numbers were calculated by the Python script in this repo. Raw spreadsheet data of both current and proposed models are also available in this repo.

Author: mosu-forge  
Key community contributors: SdoubleW, Gobble