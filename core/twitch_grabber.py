from twitch_listener import listener

bot = listener.connect_twitch('ayberkenis',
                             'oauth:baxm9a1rfekcrpuhdy4lq9uw33bi0y',
                             'th5atqzrd2olhvqphakym4rt3ask2t')

# List of channels to connect to
channels_to_listen_to = ['ayberkenis']

# Scrape live chat data into raw log files. (Duration is seconds)
bot.listen(channels_to_listen_to, duration = 1)

# Convert log files into .CSV format
bot.parse_logs(timestamp = True)

# Generate adjacency matrix
bot.adj_matrix(weighted = False, matrix_name = "streamer_network.csv")