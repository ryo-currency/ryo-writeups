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
DEV_FUND_LENGTH     = 786240 #blocks 
DEV_FUND_AMOUNT     = 8000000000000000
DEV_FUND_PER_BLOCK = DEV_FUND_AMOUNT / DEV_FUND_LENGTH
FINAL_SUBSIDY = 4000000000
COIN_EMISSION_MONTH_INTERVAL = 6 #months
COIN_EMISSION_HEIGHT_INTERVAL  = int(COIN_EMISSION_MONTH_INTERVAL * 30.4375 * 24 * 3600 / DIFFICULTY_TARGET)
HEIGHT_PER_YEAR = int((12*30.4375*24*3600)/DIFFICULTY_TARGET)
PEAK_COIN_EMISSION_YEAR = 2.5
PEAK_COIN_EMISSION_HEIGHT = HEIGHT_PER_YEAR * PEAK_COIN_EMISSION_YEAR

OUTPUT = "ryo-modified-camel.tsv"

print("Peak block height:", PEAK_COIN_EMISSION_HEIGHT)

def get_block_reward(height, coins_already_generated):
    if height < (PEAK_COIN_EMISSION_HEIGHT + COIN_EMISSION_HEIGHT_INTERVAL):
        factor = 19
        interval_num = height/COIN_EMISSION_HEIGHT_INTERVAL
        money_supply_pct = 0.1888 + interval_num*(0.023 + interval_num*0.0032)
        cal_block_reward = (MONEY_SUPPLY * money_supply_pct)/(2**factor)
    else:
        factor = 20
        cal_block_reward = (MONEY_SUPPLY - coins_already_generated)/(2**factor)
    return cal_block_reward


def calculate_emssion_speed():
    coins_generated_last_year = 1
    coins_already_generated = 0
    total_dev_fund = 0
    height = 0
    total_time = 0
    block_reward = 0
    cal_block_reward = 0
    round_factor = 10000000
    count = 0
    timestamp = START_TIMESTAMP
    
    f.write("height\tb_reward\tcoin_emitted\tcoin_emitted_w_devfund\temission_pct\temission_pct_w_dev_fee\tdev_b_reward\tdev_fund\tdev_pct_emission\tdev_pct_total\tinflation\ttimestamp\tdate\n")

    while coins_already_generated < MONEY_SUPPLY - FINAL_SUBSIDY:
        emission_speed_change_happened = False
        if height % COIN_EMISSION_HEIGHT_INTERVAL == 0:
            cal_block_reward = get_block_reward(height, coins_already_generated)
            emission_speed_change_happened = True
            count += 1
        
        if height == 0:
            block_reward = GENESIS_BLOCK_REWARD
        else:
            block_reward = int(cal_block_reward) / round_factor * round_factor
        
        if block_reward < FINAL_SUBSIDY:
            if MONEY_SUPPLY > coins_already_generated:
                block_reward = FINAL_SUBSIDY
            else:
                block_reward = FINAL_SUBSIDY/2
        
        if height >= DEV_FUND_START_HEIGHT and height < DEV_FUND_START_HEIGHT + DEV_FUND_LENGTH:
            dev_block_reward = DEV_FUND_PER_BLOCK
        else:
            dev_block_reward = 0

        total_dev_fund += dev_block_reward
        total_time += DIFFICULTY_TARGET
        timestamp += DIFFICULTY_TARGET

            
        
        coins_already_generated += block_reward
        coins_already_generated_sans_premine = coins_already_generated - PREMINE_BURN
        coins_already_generated_plus_dev_fee = coins_already_generated - PREMINE_BURN + total_dev_fund

        inflation = 0
        if emission_speed_change_happened and count % 2:
            coins_generated_this_year = coins_already_generated_plus_dev_fee - coins_generated_last_year
            inflation = coins_generated_this_year / coins_generated_last_year
            coins_generated_last_year = coins_already_generated_plus_dev_fee
        
        if int(height % (COIN_EMISSION_HEIGHT_INTERVAL/6)) == 0:
            _height = format(height, '07')
            _block_reward = '{0:.2f}'.format(block_reward/1000000000.0)
            _coins_already_generated = '{0:.2f}'.format(coins_already_generated_sans_premine/1000000000.0)
            _coins_already_generated_w_devfund = '{0:.2f}'.format(coins_already_generated_plus_dev_fee/1000000000.0)
            _emission_pct = str(round(coins_already_generated_sans_premine*100.0/MONEY_SUPPLY, 2))
            _emission_pct_w_devfund = str(round(coins_already_generated_plus_dev_fee*100.0/MONEY_SUPPLY, 2))
            _dev_block_reward = '{0:.2f}'.format(dev_block_reward/1000000000.0)
            _dev_fund = '{0:.2f}'.format(total_dev_fund/1000000000.0)
            _dev_emission_pct = str(round(total_dev_fund*100.0/coins_already_generated_plus_dev_fee, 2))
            _dev_total_pct = str(round(total_dev_fund*100.0/MONEY_SUPPLY, 2))
            _inflation_pct = str(round(inflation*100.0, 2))
            _timestamp = str(timestamp)
            _date = datetime.utcfromtimestamp(timestamp).strftime('%Y-%m-%d %H:%M:%S')
            
            f.write(_height + "\t" + _block_reward + "\t" + _coins_already_generated + "\t" + _coins_already_generated_w_devfund + "\t" + _emission_pct + "\t" + _emission_pct_w_devfund + "\t" + _dev_block_reward + "\t" + _dev_fund + "\t" + _dev_emission_pct + "\t" + _dev_total_pct + "\t" + _inflation_pct + "\t" + _timestamp + "\t" + _date + "\n")

        
        height += 1
        
    
if __name__ == "__main__":
    f = open(OUTPUT, "w")
    calculate_emssion_speed()
    f.close()
