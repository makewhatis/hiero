from hiero.tests    import BaseTestCase
from hiero.tests    import IntegrationTestBase
from pyramid        import testing
from mock           import Mock

class TestBlogController(BaseTestCase):
    def test_index_inactive(self):
        from hem.db                 import IDBSession
        from hiero.views.blog       import EntryController
        from horus.interfaces       import IUserClass
        from horus.interfaces       import IActivationClass
        from hiero.interfaces       import IHieroEntryClass
        from hiero.interfaces       import IHieroCategoryClass
        from hiero.interfaces       import IHieroSeriesClass
        from hiero.tests.models     import User
        from hiero.tests.models     import Entry
        from hiero.tests.models     import Activation
        from hiero.tests.models     import Category
        from hiero.tests.models     import Series

        self.config.registry.registerUtility(Activation, IActivationClass)
        self.config.registry.registerUtility(User, IUserClass)
        self.config.registry.registerUtility(Entry, IHieroEntryClass)
        self.config.registry.registerUtility(Category, IHieroCategoryClass)
        self.config.registry.registerUtility(Series, IHieroSeriesClass)
        self.config.registry.registerUtility(self.session, IDBSession)

        self.config.add_route('hiero_entry_index', '/')

        request = testing.DummyRequest()

        owner = User(username='sontek', email='sontek@gmail.com',
            password='foo')

        self.session.add(owner)

        entry = Entry(owner=owner, title='test entry', content='hi',
            html_content='hi<br />'
        )

        entry1 = Entry(owner=owner, title='test entry 2', content='hi',
            html_content='hi<br />'
        )

        self.session.add(entry)
        self.session.add(entry1)

        self.session.flush()

        controller = EntryController(request)

        results = controller.index()

        entries = results['entries']

        assert len(entries) == 0

    def test_index_active(self):
        from hem.db                 import IDBSession
        from hiero.views.blog       import EntryController
        from horus.interfaces       import IUserClass
        from horus.interfaces       import IActivationClass
        from hiero.interfaces       import IHieroEntryClass
        from hiero.tests.models     import User
        from hiero.tests.models     import Entry
        from hiero.tests.models     import Activation
        from hiero.tests.models     import Series
        from hiero.tests.models     import Category
        from hiero.interfaces       import IHieroCategoryClass
        from hiero.interfaces       import IHieroSeriesClass

        self.config.registry.registerUtility(Category, IHieroCategoryClass)
        self.config.registry.registerUtility(Series, IHieroSeriesClass)
        self.config.registry.registerUtility(Activation, IActivationClass)
        self.config.registry.registerUtility(User, IUserClass)
        self.config.registry.registerUtility(Entry, IHieroEntryClass)
        self.config.registry.registerUtility(self.session, IDBSession)

        self.config.add_route('hiero_entry_index', '/')

        request = testing.DummyRequest()

        owner = User(username='sontek', email='sontek@gmail.com',
                password='foo')

        self.session.add(owner)

        entry = Entry(owner=owner, title='test entry', content='hi',
            html_content='hi<br />', is_published=True
        )

        entry1 = Entry(owner=owner, title='test entry 2', content='hi',
            html_content='hi<br />', is_published=True
        )

        self.session.add(entry)
        self.session.add(entry1)

        self.session.flush()

        controller = EntryController(request)

        results = controller.index()

        entries = results['entries']

        assert len(entries) == 2
        assert entries[0] == entry
        assert entries[1] == entry1

    def test_index_active_paging(self):
        from hem.db                 import IDBSession
        from hiero.views.blog       import EntryController
        from horus.interfaces       import IUserClass
        from horus.interfaces       import IActivationClass
        from hiero.interfaces       import IHieroEntryClass
        from hiero.tests.models     import User
        from hiero.tests.models     import Entry
        from hiero.tests.models     import Activation
        from hiero.tests.models     import Category
        from hiero.tests.models     import Series
        from hiero.interfaces       import IHieroCategoryClass
        from hiero.interfaces       import IHieroSeriesClass

        self.config.registry.registerUtility(Category, IHieroCategoryClass)
        self.config.registry.registerUtility(Series, IHieroSeriesClass)

        self.config.registry.registerUtility(Entry, IHieroEntryClass)
        self.config.registry.registerUtility(self.session, IDBSession)
        self.config.registry.registerUtility(Activation, IActivationClass)
        self.config.registry.registerUtility(User, IUserClass)

        self.config.add_route('hiero_entry_index', '/')

        request = testing.DummyRequest()
        request.matchdict = Mock()

        def get(key, default):
            if key == 'page':
                return 2

        request.matchdict.get = get

        owner = User(username='sontek', email='sontek@gmail.com',
                password='foo')

        self.session.add(owner)

        entries = []

        for i in xrange(1, 21):
            entry = Entry(owner=owner, title='test entry %s' % i, content='hi',
                html_content='hi<br />%s' % i, is_published=True,
                published_on='4/%s/2012' % i
            )

            self.session.add(entry)

            entries.append(entry)

        self.session.flush()

        controller = EntryController(request)

        results = controller.index()

        result_entries = results['entries']

        assert len(result_entries) == 10
        assert entries[0].title == result_entries[9].title
        assert not entries[12] in result_entries

    def test_detail(self):
        from hem.db                 import IDBSession
        from hiero.views.blog       import EntryController
        from horus.interfaces       import IUserClass
        from horus.interfaces       import IActivationClass
        from hiero.interfaces       import IHieroEntryClass
        from hiero.tests.models     import User
        from hiero.tests.models     import Entry
        from hiero.tests.models     import Activation
        from hiero.tests.models     import Category
        from hiero.tests.models     import Series
        from hiero.interfaces       import IHieroCategoryClass
        from hiero.interfaces       import IHieroSeriesClass

        self.config.registry.registerUtility(Category, IHieroCategoryClass)
        self.config.registry.registerUtility(Series, IHieroSeriesClass)

        self.config.registry.registerUtility(Activation, IActivationClass)
        self.config.registry.registerUtility(User, IUserClass)
        self.config.registry.registerUtility(Entry, IHieroEntryClass)
        self.config.registry.registerUtility(self.session, IDBSession)

        self.config.add_route('hiero_entry_index', '/')

        request = testing.DummyRequest()
        request.matchdict = Mock()

        owner = User(username='sontek', email='sontek@gmail.com',
            password='foo')

        self.session.add(owner)

        entry = Entry(owner=owner, title='test entry', content='hi',
            html_content='hi<br />', is_published=True
        )

        entry1 = Entry(owner=owner, title='test entry 2', content='hi',
            html_content='hi<br />', is_published=True
        )

        self.session.add(entry)
        self.session.add(entry1)

        self.session.flush()

        def get(key, default):
            if key == 'slug':
                return entry1.slug

        request.matchdict.get = get

        controller = EntryController(request)

        results = controller.detail()

        returned_entry = results['entry']
        returned_entry == entry

class TestBlogIntegrationViews(IntegrationTestBase):
    def test_index(self):
        """ Call the index view, make sure routes are working """
        from hiero.tests.models     import User
        from hiero.tests.models     import Entry

        owner = User(username='sontek', email='sontek@gmail.com',
            password='foo')


        entry = Entry(owner=owner, title='test entry', content='hi',
            html_content='hi<br />foo', is_published=True
        )

        entry1 = Entry(owner=owner, title='test entry 1', content='hi',
            html_content='hi<br />bar', is_published=True
        )

        self.session.add(owner)
        self.session.add(entry)
        self.session.add(entry1)

        res = self.app.get('/')
        assert res.status_int == 200
        assert 'foo' in res.body
        assert 'bar' in res.body

    def test_detail(self):
        """ Call the detail view, make sure routes are working """
        from hiero.tests.models     import User
        from hiero.tests.models     import Entry

        owner = User(username='sontek', email='sontek@gmail.com',
                password='foo')


        entry = Entry(owner=owner, title='test entry', content='hi',
            html_content='hi<br />', is_published=True
        )

        self.session.add(owner)
        self.session.add(entry)
        self.session.flush()

        res = self.app.get('/detail/test-entry')
        assert res.status_int == 200
        assert 'hi' in res.body
