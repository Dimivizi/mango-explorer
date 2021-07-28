import typing

from solana.publickey import PublicKey

from .context import mango
from .fakes import fake_account_info, fake_seeded_public_key

from decimal import Decimal


def test_constructor():
    address = fake_seeded_public_key("perp event queue address")
    account_info: mango.AccountInfo = fake_account_info(address)
    meta_data: mango.Metadata = mango.Metadata(mango.layouts.DATA_TYPE.EventQueue, mango.Version.V1, True)
    head: Decimal = Decimal(0)
    count: Decimal = Decimal(0)
    sequence_number: Decimal = Decimal(0)
    events: typing.Sequence[typing.Optional[mango.PerpEvent]] = []

    actual = mango.PerpEventQueue(account_info, mango.Version.V1, meta_data, head, count, sequence_number, events)
    assert actual is not None
    assert actual.logger is not None
    assert actual.account_info == account_info
    assert actual.meta_data == meta_data
    assert actual.address == address
    assert actual.head == head
    assert actual.count == count
    assert actual.sequence_number == sequence_number
    assert actual.events == events


def _fake_pev(head: Decimal, count: Decimal, events: typing.Sequence[typing.Optional[mango.PerpEvent]]) -> mango.PerpEventQueue:
    address = fake_seeded_public_key("perp event queue address")
    account_info: mango.AccountInfo = fake_account_info(address)
    meta_data: mango.Metadata = mango.Metadata(mango.layouts.DATA_TYPE.EventQueue, mango.Version.V1, True)
    sequence_number: Decimal = Decimal(0)
    return mango.PerpEventQueue(account_info, mango.Version.V1, meta_data, head, count, sequence_number, events)


class TstPE(mango.PerpEvent):
    def __init__(self, event_type: int = 25):
        super().__init__(event_type)

    @property
    def accounts_to_crank(self) -> typing.Sequence[PublicKey]:
        return []

    def __str__(self):
        return f"« TstPE [{self.event_type}] »"


def test_unseen_with_no_changes():
    initial = _fake_pev(Decimal(5), Decimal(2), [TstPE(), TstPE(), TstPE(), TstPE(), TstPE()])
    actual: mango.UnseenPerpEventChangesTracker = mango.UnseenPerpEventChangesTracker(initial)
    assert actual.last_head == Decimal(5)

    updated = _fake_pev(Decimal(5), Decimal(2), [TstPE(), TstPE(), TstPE(), TstPE(), TstPE()])
    unseen = actual.unseen(updated)
    assert len(unseen) == 0
    assert actual.last_head == Decimal(5)


def test_unseen_with_one_unprocessed_change():
    initial = _fake_pev(Decimal(1), Decimal(0), [TstPE(), TstPE(), TstPE(), TstPE(), TstPE()])
    actual: mango.UnseenPerpEventChangesTracker = mango.UnseenPerpEventChangesTracker(initial)
    assert actual.last_head == Decimal(1)

    marker = TstPE(50)
    updated = _fake_pev(Decimal(2), Decimal(1), [TstPE(), marker, TstPE(), TstPE(), TstPE()])
    unseen = actual.unseen(updated)
    assert actual.last_head == Decimal(2)
    assert len(unseen) == 1
    assert unseen[0] == marker


def test_unseen_with_two_unprocessed_changes():
    initial = _fake_pev(Decimal(1), Decimal(0), [TstPE(), TstPE(), TstPE(), TstPE(), TstPE()])
    actual: mango.UnseenPerpEventChangesTracker = mango.UnseenPerpEventChangesTracker(initial)
    assert actual.last_head == Decimal(1)

    marker1 = TstPE(50)
    marker2 = TstPE(51)
    updated = _fake_pev(Decimal(3), Decimal(2), [TstPE(), marker1, marker2, TstPE(), TstPE()])
    unseen = actual.unseen(updated)
    assert actual.last_head == Decimal(3)
    assert len(unseen) == 2
    assert unseen[0] == marker1
    assert unseen[1] == marker2


def test_unseen_with_two_processed_changes():
    # This should be identical to the previous test - it shouldn't matter to 'seen' tracking whether an event
    # is processed or not.
    initial = _fake_pev(Decimal(1), Decimal(0), [TstPE(), TstPE(), TstPE(), TstPE(), TstPE()])
    actual: mango.UnseenPerpEventChangesTracker = mango.UnseenPerpEventChangesTracker(initial)
    assert actual.last_head == Decimal(1)

    marker1 = TstPE(50)
    marker2 = TstPE(51)
    updated = _fake_pev(Decimal(3), Decimal(0), [TstPE(), marker1, marker2, TstPE(), TstPE()])
    unseen = actual.unseen(updated)
    assert actual.last_head == Decimal(3)
    assert len(unseen) == 2
    assert unseen[0] == marker1
    assert unseen[1] == marker2


def test_unseen_with_two_unprocessed_changes_wrapping_around():
    # This is tricky because the change overlaps the end of the array-as-ringbuffer. A change is added
    # to the next slot (which is the last slot in the array) and then another is added to the next slot
    # (which is the first slot in the array). Seen tracking shouldn't care - it should just return the
    # unseen events in the proper order.
    initial = _fake_pev(Decimal(4), Decimal(0), [TstPE(), TstPE(), TstPE(), TstPE(), TstPE()])
    actual: mango.UnseenPerpEventChangesTracker = mango.UnseenPerpEventChangesTracker(initial)
    assert actual.last_head == Decimal(4)

    marker1 = TstPE(50)
    marker2 = TstPE(51)
    updated = _fake_pev(Decimal(1), Decimal(2), [marker2, TstPE(), TstPE(), TstPE(), marker1])
    unseen = actual.unseen(updated)
    assert actual.last_head == Decimal(1)
    assert len(unseen) == 2
    assert unseen[0] == marker1
    assert unseen[1] == marker2