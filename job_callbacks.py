import datetime
import config
import tariffs
from models import User


def reward_users(bot):
    levels_percentage = tariffs.get_referral_levels_percentage()
    deposit_reward = User.deposit * User.deposit_reward
    query = User.update(
        balance=(
                User.balance
                + User.deposit * User.deposit_reward
                + User.first_level_partners_deposit * User.deposit_reward * levels_percentage[0]
                + User.second_level_partners_deposit * User.deposit_reward * levels_percentage[1]
                + User.third_level_partners_deposit * User.deposit_reward * levels_percentage[2]
        ),
        sum_deposit_reward=User.sum_deposit_reward + deposit_reward
    ).where(User.deposit >= tariffs.eth_minimal_deposit())
    query.execute()

    users = User.select().where(User.deposit >= tariffs.eth_minimal_deposit())

    for user in users:
        deposit_reward = user.deposit * user.deposit_reward
        first_level_reward = user.first_level_partners_deposit * user.deposit_reward * levels_percentage[0]
        second_level_reward = user.second_level_partners_deposit * user.deposit_reward * levels_percentage[1]
        third_level_reward = user.third_level_partners_deposit * user.deposit_reward * levels_percentage[2]

        bot.send_message(
            chat_id=user.chat_id,
            text=f'You received accruals:\n'
                 f'Deposit: {deposit_reward:.7f} ETH\n'
                 f'1 level: {first_level_reward:.7f} ETH\n'
                 f'2 level: {second_level_reward:.7f} ETH\n'
                 f'3 level: {third_level_reward:.7f} ETH'
        )


def notify_inactive_users(bot):
    four_days_ago = datetime.datetime.now() - datetime.timedelta(days=4)
    inactive_users = User.select(User.chat_id).where(
        (User.created_at < four_days_ago) & (User.deposit < tariffs.eth_minimal_deposit())
    )

    text = f'We see that you have not yet started earning with us.\n' \
           f'If you have any questions - write to us in technical support and we will help:\n' \
           f'{config.get_support_account()}'
    for user in inactive_users:
        bot.send_message(
            chat_id=user.chat_id,
            text=text
        )
