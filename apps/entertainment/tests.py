import random
import shutil
import tempfile
from os import path

from django.db.models import Sum, Count
from django.test import TestCase

from apps.user.models import User
from apps.entertainment.models import Channel, Content, MetaData, Rating, Group
from apps.utils import recursive_average_calculator


class ChannelModelTestCase(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.user = User.objects.create(
            username='can',
            first_name='Can',
            last_name='Adiyaman'
        )
        cls.user.set_password('122333')

    def setUp(self) -> None:
        self.test_dir = tempfile.mkdtemp()

    def tearDown(self):
        shutil.rmtree(self.test_dir)

    def test_crud_channel(self):

        # create test
        channel = Channel.objects.create(
            title='A',
            language='tr',
            created_by=self.user
        )

        self.assertEqual(channel.pk, channel.id)

        # read test
        channel = Channel.objects.get(id=channel.id)

        self.assertEqual(channel.slug, 'a')

        # update test
        channel = Channel.objects.get(id=channel.id)
        channel.title = 'changed A'
        channel.save()
        channel = Channel.objects.get(id=channel.id)

        self.assertEqual(channel.title, 'changed A')

        # delete test
        channel = Channel.objects.first()
        delete = channel.delete()

        self.assertEqual(str(delete), "(1, {'entertainment.Channel': 1})")

    def test_crud_content(self):

        # create test
        with open(path.join(self.test_dir, 'test.txt'), 'w') as f:
            f.write('The owls are not what they seem')

        with open(path.join(self.test_dir, 'test.txt')) as f:
            content = Content.objects.create(
                file=f.name,
                created_by=self.user,
                filename='test'
            )

        self.assertEqual(content.pk, content.id)

        # read test
        content = Content.objects.get(id=content.id)

        self.assertEqual(content.filename, 'test')

        # update test
        content = Content.objects.get(id=content.id)
        content.filename = 'changed_test'
        content.save()
        content = Content.objects.get(id=content.id)

        self.assertEqual(content.filename, 'changed_test')

        # delete test
        content = Content.objects.first()
        delete = content.delete()

        self.assertEqual(str(delete), "(1, {'entertainment.Content': 1})")

    def test_crud_metadata(self):

        # create test
        with open(path.join(self.test_dir, 'test.txt'), 'w') as f:
            f.write('The owls are not what they seem')

        with open(path.join(self.test_dir, 'test.txt')) as f:
            content = Content.objects.create(
                file=f.name,
                created_by=self.user,
                filename='test'
            )


        meta_data = MetaData.objects.create(
            content=content,
            key='Author',
            value='Can ADIYAMAN'
        )

        self.assertEqual(meta_data.pk, meta_data.id)

        # read test
        meta_data = MetaData.objects.get(id=meta_data.id)

        self.assertEqual(meta_data.key, 'Author')

        # update test
        meta_data = MetaData.objects.get(id=meta_data.id)

        meta_data.value = 'Changed Can ADIYAMAN'
        meta_data.save()

        meta_data = MetaData.objects.get(id=meta_data.id)

        self.assertEqual(meta_data.value, 'Changed Can ADIYAMAN')

        # delete test
        delete = meta_data.delete()

        self.assertEqual(str(delete), "(1, {'entertainment.MetaData': 1})")

    def test_crud_rating(self):
        # create test
        with open(path.join(self.test_dir, 'test.txt'), 'w') as f:
            f.write('The owls are not what they seem')

        with open(path.join(self.test_dir, 'test.txt')) as f:
            content = Content.objects.create(
                file=f.name,
                created_by=self.user,
                filename='test'
            )

        rating = Rating.objects.create(
            content=content,
            user=self.user,
            rate=8
        )

        self.assertEqual(rating.pk, rating.id)

        # read test
        rating = Rating.objects.get(id=rating.id)

        self.assertEqual(rating.rate, 8)

        # update test
        rating = Rating.objects.get(id=rating.id)

        rating.rate = 6
        rating.save()

        rating = Rating.objects.get(id=rating.id)

        self.assertEqual(rating.rate, 6)

        # delete test
        delete = rating.delete()

        self.assertEqual(str(delete), "(1, {'entertainment.Rating': 1})")

    def test_insert_content_to_channel(self):
        channel = Channel.objects.create(
            title='A',
            language='tr',
            created_by=self.user
        )

        with open(path.join(self.test_dir, 'test.txt'), 'w') as f:
            f.write('The owls are not what they seem')
            content = Content.objects.create(
                file=f.name,
                created_by=self.user,
                filename='test'
            )

        self.assertEqual(
            channel.contents.count(),
            0
        )

        channel.contents.add(content)

        channel = Channel.objects.get(id=channel.id)
        self.assertEqual(
            channel.contents.count(),
            1
        )

    def test_add_metadata_to_content(self):
        with open(path.join(self.test_dir, 'test.txt'), 'w') as f:
            f.write('The owls are not what they seem')
            content = Content.objects.create(
                file=f.name,
                created_by=self.user,
                filename='test'
            )

        meta_data_1 = MetaData.objects.create(
            content=content, key='Author', value='Jhon Doe'
        )

        meta_data_2 = MetaData.objects.create(
            content=content, key='Genre', value='Comedy'
        )

        content = Content.objects.get(id=content.id)

        self.assertEqual(
            list(content.metadatas.values('key', 'value')),
            [
                {'key': meta_data_1.key, 'value': meta_data_1.value},
                {'key': meta_data_2.key, 'value': meta_data_2.value}
            ]
        )

    def test_add_rating_to_content(self):
        with open(path.join(self.test_dir, 'test.txt'), 'w') as f:
            f.write('The owls are not what they seem')
            content = Content.objects.create(
                file=f.name,
                created_by=self.user,
                filename='test'
            )

        user_1 = User.objects.create(
            username=f'test_user_1',
            first_name=f'First Name 1',
            last_name=f'Last Name 1'
        )
        Rating.objects.create(
            user=user_1,
            content=content,
            rate=random.randint(0, 10)
        )

        user_2 = User.objects.create(
            username=f'test_user_2',
            first_name=f'First Name 2',
            last_name=f'Last Name 2'
        )
        Rating.objects.create(
            user=user_2,
            content=content,
            rate=random.randint(0, 10)
        )

        self.assertEqual(
            content.content_ratings.count(),
            2
        )

    def test_calculate_content_average_rate(self):
        with open(path.join(self.test_dir, 'test.txt'), 'w') as f:
            f.write('The owls are not what they seem')
            content = Content.objects.create(
                file=f.name,
                created_by=self.user,
                filename='test'
            )

        for i in range(0, 20):
            user = User.objects.create(
                username=f'test_user_{i}',
                first_name=f'First Name {i}',
                last_name=f'Last Name {i}'
            )

            Rating.objects.create(
                user=user,
                content=content,
                rate=5
            )

        self.assertEqual(
            list(content.content_ratings.values('content_id').annotate(
                average=Sum('rate') / Count('id'))),
            [{'content_id': 1, 'average': 5}]
        )

    def test_calculate_channel_average_rate_by_contents(self):

        with open(path.join(self.test_dir, 'test.txt'), 'w') as f:
            f.write('The owls are not what they seem')
            content = Content.objects.create(
                file=f.name,
                created_by=self.user,
                filename='test'
            )

        for i in range(0, 30):
            user = User.objects.create(
                username=f'test_user_{i}',
                first_name=f'First Name {i}',
                last_name=f'Last Name {i}'
            )

            Rating.objects.create(
                user=user,
                content=content,
                rate=9
            )
        channel = Channel.objects.create(
            title='Foo',
            language='tr',
            created_by=self.user
        )
        channel.contents.add(content)

        # testing channel rating 1.Step: by contents
        channel = Channel.objects.get(id=channel.id)

        self.assertTrue(channel.contents.exists())

        rating = Rating.objects \
            .filter(content__channels=channel) \
            .values('content_id') \
            .annotate(average=Sum('rate') / Count('id'))
        self.assertEqual(
            rating.first(),
            {'content_id': 1, 'average': 9}
        )

    def test_calculate_channel_average_rate_by_subchannels(self):

        main_channel = Channel.objects.create(
            title='Series',
            language='en-gb',
            created_by=self.user
        )
        first_step_channel = Channel.objects.create(
            title='Atresplayer',
            language='en-gb',
            created_by=self.user,
            parent=main_channel
        )
        second_step_channel = Channel.objects.create(
            title='El club de la comedia',
            language='en-gb',
            created_by=self.user,
            parent=first_step_channel
        )


        with open(path.join(self.test_dir, 'test_1.txt'), 'w') as f:
            f.write('The owls are not what they seem')
            content_1 = Content.objects.create(
                file=f.name,
                created_by=self.user,
                filename='test_1'
            )

        with open(path.join(self.test_dir, 'test_2.txt'), 'w') as f:
            f.write('The owls are not what they seem')
            content_2 = Content.objects.create(
                file=f.name,
                created_by=self.user,
                filename='test_2'
            )

        second_step_channel.contents.add(content_1)
        second_step_channel.contents.add(content_2)

        for i in range(0, 10):
            user = User.objects.create(
                username=f'test_user_{i}',
                first_name=f'First Name {i}',
                last_name=f'Last Name {i}'
            )

            for content in second_step_channel.contents.all():
                Rating.objects.create(
                    user=user,
                    content=content,
                    rate=i
                )

        # testing channel rating 1.Step: by contents
        main_channels = Channel.objects.filter(parent=None)

        # we know we have only one parent, so I didn't loop. Just take first one.
        # for main_channel in main_channels:
        #     main_channel.subchannels.all()
        #     ...

        series_channel = main_channels.first()

        # Now we'll calculate entire series root all subchannels and self.
        calculates_averages = []  # {"channel_title": "Series", average: 9}
        recursive_average_calculator(series_channel, calculates_averages)

        self.assertEqual(
            calculates_averages,
            [
             {'title': 'El club de la comedia', 'average': 4},
             {'title': 'Atresplayer', 'average': 4},
             {'title': 'Series', 'average': 4}
            ]
        )

    def test_crud_group(self):
        # create test
        group = Group.objects.create(title='test')

        self.assertEqual(group.pk, group.id)

        # read test
        group = Group.objects.get(id=group.id)

        self.assertEqual(group.title, 'test')

        # update test
        group = Group.objects.get(id=group.id)
        group.title = 'changed title'
        group.save()
        group = Group.objects.get(id=group.id)

        self.assertEqual(group.title, 'changed title')

        # delete test
        group = Group.objects.first()
        delete = group.delete()

        self.assertEqual(str(delete), "(1, {'entertainment.Group': 1})")

    def test_update_group_channels_method(self):
        channel = Channel.objects.create(
            title='parent',
            language='tr',
            created_by=self.user
        )
        sub_channel_1 = Channel.objects.create(
            title='sub channel 1',
            language='tr',
            created_by=self.user,
            parent=channel
        )

        Channel.objects.create(
            title='sub channel 2',
            language='tr',
            created_by=self.user,
            parent=sub_channel_1
        )

        Channel.objects.create(
            title='sub channel 1_1',
            language='tr',
            created_by=self.user,
            parent=channel
        )

        the_group = Group.objects.create(title='test')

        channel.update_group_channels(group_ids=[the_group.id], insert=True)

        self.assertEqual(
            list(the_group.channels_by_group.values_list('title', flat=True)),
            ['parent', 'sub channel 1', 'sub channel 2', 'sub channel 1_1']
        )

        channel.update_group_channels(group_ids=[the_group.id], insert=False)
        self.assertEqual(
            list(the_group.channels_by_group.values_list('title', flat=True)),
            []
        )
