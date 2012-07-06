from hiero.tests    import BaseTestCase
from pyramid        import testing
from mock           import Mock

class TestBlogController(BaseTestCase):
    def test_index_inactive(self):
        from hem.db                 import IDBSession
        from hiero.views.blog       import EntryController
        from horus.interfaces       import IHorusUserClass
        from horus.interfaces       import IHorusActivationClass
        from hiero.interfaces       import IHieroEntryClass
        from hiero.tests.models     import User
        from hiero.tests.models     import Entry
        from hiero.tests.models     import Activation

        self.config.registry.registerUtility(Activation, IHorusActivationClass)
        self.config.registry.registerUtility(User, IHorusUserClass)
        self.config.registry.registerUtility(Entry, IHieroEntryClass)
        self.config.registry.registerUtility(self.session, IDBSession)

        self.config.add_route('hiero_entry_index', '/')

        request = testing.DummyRequest()

        owner = User(user_name='sontek', email='sontek@gmail.com')
        owner.set_password('foo')

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
        from horus.interfaces       import IHorusUserClass
        from horus.interfaces       import IHorusActivationClass
        from hiero.interfaces       import IHieroEntryClass
        from hiero.tests.models     import User
        from hiero.tests.models     import Entry
        from hiero.tests.models     import Activation

        self.config.registry.registerUtility(Activation, IHorusActivationClass)
        self.config.registry.registerUtility(User, IHorusUserClass)
        self.config.registry.registerUtility(Entry, IHieroEntryClass)
        self.config.registry.registerUtility(self.session, IDBSession)

        self.config.add_route('hiero_entry_index', '/')

        request = testing.DummyRequest()

        owner = User(user_name='sontek', email='sontek@gmail.com')
        owner.set_password('foo')

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

    def test_detail(self):
        from hem.db                 import IDBSession
        from hiero.views.blog       import EntryController
        from horus.interfaces       import IHorusUserClass
        from horus.interfaces       import IHorusActivationClass
        from hiero.interfaces       import IHieroEntryClass
        from hiero.tests.models     import User
        from hiero.tests.models     import Entry
        from hiero.tests.models     import Activation

        self.config.registry.registerUtility(Activation, IHorusActivationClass)
        self.config.registry.registerUtility(User, IHorusUserClass)
        self.config.registry.registerUtility(Entry, IHieroEntryClass)
        self.config.registry.registerUtility(self.session, IDBSession)

        self.config.add_route('hiero_entry_index', '/')

        request = testing.DummyRequest()
        request.matchdict = Mock()

        owner = User(user_name='sontek', email='sontek@gmail.com')
        owner.set_password('foo')

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

