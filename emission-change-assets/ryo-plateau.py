#!/bin/python

from datetime import datetime

START_TIMESTAMP = 1492486495
EMISSION_SPEED_FACTOR = 19
DIFFICULTY_TARGET = 240 # seconds
MONEY_SUPPLY         = 88888888000000000
GENESIS_BLOCK_REWARD     = 8800000000000000
PREMINE_REMAIN = 99948553572999
PREMINE_BURN     = GENESIS_BLOCK_REWARD - PREMINE_REMAIN
DEV_FUND_START_HEIGHT  = 165000
DEV_FUND_LENGTH     = 786240 # blocks 
DEV_FUND_AMOUNT     = 8000000000000000
DEV_FUND_PER_BLOCK = DEV_FUND_AMOUNT / DEV_FUND_LENGTH
FINAL_SUBSIDY = 4000000000

HEIGHT_PER_YEAR = int((12*30.4375*24*3600)/DIFFICULTY_TARGET)

COIN_EMISSION_MONTH_INTERVAL = 6 # months
COIN_EMISSION_HEIGHT_INTERVAL  = int(COIN_EMISSION_MONTH_INTERVAL * 30.4375 * 24 * 3600 / DIFFICULTY_TARGET)
PEAK_COIN_EMISSION_YEAR = 2.5 # years
PEAK_COIN_EMISSION_LENGTH = 1.5 # years
PEAK_COIN_EMISSION_HEIGHT = HEIGHT_PER_YEAR * PEAK_COIN_EMISSION_YEAR
PEAK_COIN_EMISSION_HEIGHT_END = HEIGHT_PER_YEAR * PEAK_COIN_EMISSION_LENGTH + PEAK_COIN_EMISSION_HEIGHT


OUTPUT = "ryo-plateau.tsv"

def get_block_reward(height):
    round_factor = 10000000

    if height == 0:
        base_reward = GENESIS_BLOCK_REWARD - PREMINE_BURN
    elif height < PEAK_COIN_EMISSION_HEIGHT_END:
        interval_num = int(min(height, PEAK_COIN_EMISSION_HEIGHT) / COIN_EMISSION_HEIGHT_INTERVAL)
        money_supply_pct = 0.1888 + interval_num*(0.023 + interval_num*0.0032)
        base_reward = (MONEY_SUPPLY * money_supply_pct)/(2**EMISSION_SPEED_FACTOR)
    else:
        interval_num = int((height - PEAK_COIN_EMISSION_HEIGHT_END) / COIN_EMISSION_HEIGHT_INTERVAL)
        base_reward = get_block_reward(PEAK_COIN_EMISSION_HEIGHT)
        for n in range(interval_num + 1):
            base_reward -= int((base_reward * 705) / 10000)
            if base_reward < FINAL_SUBSIDY:
                break

    base_reward = int(base_reward / round_factor ) * round_factor

    if base_reward < FINAL_SUBSIDY:
        base_reward = FINAL_SUBSIDY
    
    return base_reward


def calculate_emssion_speed():
    height = 0
    block_reward = 0
    circ_supply = 0
    dev_fund = 0
    coins_generated_last_year = 1
    timestamp = START_TIMESTAMP
    
    f.write("height\tblock_reward\tcoin_emitted\temission_pct\tdev_fund\tdev_pct_emission\tinflation\ttimestamp\tdate\n")

    while circ_supply < MONEY_SUPPLY:

        block_reward = get_block_reward(height)
        
        if height >= DEV_FUND_START_HEIGHT and height < DEV_FUND_START_HEIGHT + DEV_FUND_LENGTH:
            dev_block_reward = DEV_FUND_PER_BLOCK
        else:
            dev_block_reward = 0

        dev_fund += dev_block_reward
        circ_supply += block_reward + dev_block_reward

        inflation = 0
        if int(height % (COIN_EMISSION_HEIGHT_INTERVAL*2)) == 0:
            coins_generated_this_year = circ_supply - coins_generated_last_year
            inflation = coins_generated_this_year / coins_generated_last_year
            coins_generated_last_year = circ_supply
        
        if int(height % (COIN_EMISSION_HEIGHT_INTERVAL/6)) == 0:
            _height = format(height, '07')
            _block_reward = '{0:.2f}'.format(block_reward/1000000000.0)
            _circ_supply = '{0:.2f}'.format(circ_supply/1000000000.0)
            _emission_pct = str(round(circ_supply*100.0/MONEY_SUPPLY, 2))
            _dev_fund = '{0:.2f}'.format(dev_fund/1000000000.0)
            _dev_emission_pct = str(round(dev_fund*100.0/circ_supply, 2))
            _inflation_pct = str(round(inflation*100.0, 2))
            _timestamp = str(timestamp)
            _date = datetime.utcfromtimestamp(timestamp).strftime('%Y-%m-%d %H:%M:%S')
            
            f.write(_height + "\t" + _block_reward + "\t" + _circ_supply + "\t" + _emission_pct + "\t" + _dev_fund + "\t" + _dev_emission_pct + "\t" + _inflation_pct + "\t" + _timestamp + "\t" + _date + "\n")

        
        timestamp += DIFFICULTY_TARGET
        height += 1
        
    
if __name__ == "__main__":
    f = open(OUTPUT, "w")
    calculate_emssion_speed()
    f.close()
