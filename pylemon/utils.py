from pylemon.types import ChannelType, TextChannel, VoiceChannel, DMChannel, CategoryChannel


def deserialize_channel(bot, guild_id ,channel_data:dict):
    channelType = channel_data['type']
    if channelType == ChannelType.GUILD_TEXT:
        return TextChannel(bot,guild_id,channel_data)
    elif channelType == ChannelType.GUILD_VOICE:
        return VoiceChannel(bot,guild_id,channel_data)
    elif channelType == ChannelType.DM:
        return DMChannel(bot,guild_id,channel_data)
    elif channelType == ChannelType.GUILD_CATEGORY:
        return CategoryChannel(bot,guild_id,channel_data)
    else:
        pass