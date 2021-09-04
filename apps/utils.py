from django.db.models import Sum, Count, F

from apps.entertainment.models import Rating, Channel


__all__ = ['recursive_average_calculator']


def recursive_average_calculator(root_channel: Channel, result_list: list):

    if root_channel.subchannels.exists():
        _tmp_subchannel_averages = []  # This list keeps subchannel averages temporary

        for sub_channel in root_channel.subchannels.all():
            sub_rate = recursive_average_calculator(sub_channel, result_list)
            _tmp_subchannel_averages.append(sub_rate)

        if len(_tmp_subchannel_averages) >= 1:
            _tmp_subchannel_average = {
                'title': root_channel.title,
                'average': sum([_tmp['average']for _tmp in _tmp_subchannel_averages])
            }
            result_list.append(_tmp_subchannel_average)
            return _tmp_subchannel_average
        return {'title': root_channel.title, 'average': 0}

    elif root_channel.contents.exists():
        rating = Rating.objects \
            .filter(content__channels=root_channel)\
            .values(title=F('content__channels__title')) \
            .annotate(average=Sum('rate') / Count('id'))
        result_list.append(rating[0])
        return rating[0]

    else:
        return {'title': root_channel.title, 'average': 0}
