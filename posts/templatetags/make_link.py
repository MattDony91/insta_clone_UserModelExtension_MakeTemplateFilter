from django import template
import re

register = template.Library()

@register.filter
def hashtag_link(post):
    content = post.content
    hashtags = post.hashtags.all()

    for hashtag in hashtags:
        # content = content.replace(
        #     f'{hashtag.content}',
        #     f'<a href="/posts/hashtags/{hashtag.id}/">{hashtag.content}</a>'
        # )
        content = re.sub(
            fr'{hashtag.content}\b', # 정규 표현식
            f'<a href="/posts/hashtags/{hashtag.id}/">{hashtag.content}</a>',
            content
        )
    return content