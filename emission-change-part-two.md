# Ryo Emission Change Discussion Part Two

**Published April 24th, 2019**

[Ryo Emission Change Discussion Part One](https://github.com/ryo-currency/ryo-writeups/blob/master/emission-change.md)

## Preface

After publishing the initial proposed emission curve, there were numerous suggestions to model out a similar curve, but with the block reward hitting a plateau instead of a peak. This model was suggested in order to lengthen the discovery time for miners before block rewards started dropping. This is to compensate for making the peak occur earlier in the coin's history. This document outlines two plateau curves with the peak lasting 12 and 18 months.

There are a few important points that were discovered after publishing the initial proposed emission curve that this new model addresses. First, the original Sumokoin curve had always advertised a stepped curve where block rewards changed every six months. This was not true on the decline portion of the curve which was programmed to re-calculate each block, thus making a smooth decline after the peak. Second, due to the way the decline portion of the curve was programmed, the total supply only hit 86 million coins before tail emission.

These new models corrects the decline portion of the curve to make it stepped, as well as hitting 88 million coins as intended.

Interactive charts are [available online.](https://www.ryoblocks.com/emission-charts/)

## Plateau curve details

These new models follow the previously proposed curve with a maximum block reward of 65.07 coins. Once this maximum is reached, the block reward will remain there for an extended period of time, then start to decrease. In the first model, the plateau lasts 12 months and then decreases by 6.55% every six months until hitting the tail emission of 4 coins per block. In the second model, the plateau lasts 18 months and then decreases by 7.05% every six months until tail emission.

## Block reward in detail

![Block reward chart](emission-change-assets/chart-block-reward-plateau.png?raw=true "Block reward chart")

The above graph shows the current block reward schedule (blue), the originally proposed change (green), a 12 month plateau model (yellow), and an 18 month plateau (magenta) over 20 years. In each case, the block rewards will continue as scheduled until about April 2020, only diverging at block 394470.

The plateau models are meant to extend the peak giving miners more chance to discover the project before rewards start declining. The area under the old curves (blue and green) are different from the plateau curves (yellow and magenta) because of the correction in total emission before tail reward.

## Inflation percentage in detail

![Inflation chart](emission-change-assets/chart-inflation-plateau.png?raw=true "Inflation chart")

This graph shows the annual inflation by year. The plateau models show slightly higher inflation than the previously proposed model, but still have a significant reduction over the current model.

## Emission percentage in detail

![Emission chart](emission-change-assets/chart-emission-plateau.png?raw=true "Emission chart")

With the 12 month plateau model, 99% emission will be reached in the year 2041. With the 18 month plateau model, 99% emission will be reached in the year 2040. This is opposed to 99% emission being reached in the year 2036 in the current model, and 2048 in the previously proposed model. However in both the current and previously proposed models, tail emission was activated before the emission reached 88 million coins. In the plateau models, tail emission correctly kicks in right as the regular emission reaches 88 million coins.

## Development fund

![Development fund chart](emission-change-assets/chart-development-fund-plateau.png?raw=true "[Development fund chart")

As described in the previous write up, the slower emission makes the development fund temporarily be a higher percentage of the circulating supply. With the 12 month plateau curve, the development fund reaches a maximum of 14.52% in the year 2024. With the 18 month plateau curve, the development fund reaches a maximum of 14.19%. This is opposed to a maximum of 11.98% in the current curve, and  15.21% in the previously proposed curve.

As always, the development fund does not change, and will reach 9% total when tail emission starts.

## How does this compare to Bitcoin or Monero?

### Block reward

![Block reward chart](emission-change-assets/chart-block-reward-with-bitcoin-monero-plateau.png?raw=true "Block reward chart")

### Inflation

![Inflation chart](emission-change-assets/chart-inflation-with-bitcoin-monero-plateau.png?raw=true "Inflation chart")

### Emission

![Emission chart](emission-change-assets/chart-emission-with-bitcoin-monero-plateau.png?raw=true "Emission chart")

## Conclusion

There was some very valuable community feedback after the initial emission change proposal was created. Besides the viewpoint that emission should never change after the genesis block, the short peak seemed to be the only concern. 

The purpose of this proposal is to again gather feedback on the fundamentals of changing emission in general, and if this new proposed plateau model accomplishes improving the monetary policy of Ryo.

These numbers were calculated by the [Python script](https://github.com/mosu-forge/ryo-writeups/blob/topic-emission/emission-change-assets/ryo-plateau.py) in this repo. Raw spreadsheet data ([Excel](https://github.com/mosu-forge/ryo-writeups/raw/topic-emission/emission-change-assets/ryo-modified-camel-and-plateau.xlsx), [Gnumeric](https://github.com/mosu-forge/ryo-writeups/raw/topic-emission/emission-change-assets/ryo-modified-camel-and-plateau.gnumeric)) of both current and proposed models are also available in this repo.

Author: mosu-forge  
Key community contributors: SdoubleW, Gobble, mitchellpkt, CryptoContra