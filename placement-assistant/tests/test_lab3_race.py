"""Lab 3 — two runs booking the same slot; one wins cleanly.

TODO: write these tests yourself. Delete the skip line when you start.

1. test_two_workers_two_runs_one_slot
   Two students who are both eligible for TCS (22IT017 and 22CS045) each get a thread and a queued run.
   Each run applies to drive 2 and books slot 3 (build the model turns with PositionalMock).
   Use two RunStore and two PlacementDb connections on the same files (the db_files fixture), and one Worker
   per connection. Assert: both runs SUCCEED (losing a race is not a crash), exactly one book_interview_slot
   result is "booked", the other is the "slot_taken" error, and slot 3 holds exactly one student.

2. test_truly_concurrent_claims_have_one_winner
   Both students apply to drive 2. Read slot 3's version once. Start 8 threads, each with its OWN
   PlacementDb connection, held at a threading.Barrier, then all call claim_slot(3, student, version).
   Assert exactly one True, seven False, and the version went up by exactly one.
"""
import pytest

import threading

from app.memory import RunStore
from app.placement_db import PlacementDb
from app.providers import PositionalMock, ModelTurn, ToolCall
from app.tools.placement_tools import PlacementTools
from app.worker import Worker


def booking_run(student):
    return PositionalMock([
        ModelTurn(text=None, tool_calls=[ToolCall("apply_to_drive", {"student_id": student, "drive_id": 2})]),
        ModelTurn(text=None, tool_calls=[ToolCall("book_interview_slot", {"student_id": student, "slot_id": 3})]),
        ModelTurn(text="done"),
    ])


def test_two_workers_two_runs_one_slot(db_files, clock):
    agent, place = db_files
    store_a, store_b = RunStore(agent, clock), RunStore(agent, clock)
    run_a = store_a.enqueue(store_a.create_thread("22IT017"), "book TCS", "mock")
    run_b = store_b.enqueue(store_b.create_thread("22CS045"), "book TCS", "mock")
    Worker(store_a, PlacementDb(place), booking_run("22IT017"), worker_id="A").run_once()
    Worker(store_b, PlacementDb(place), booking_run("22CS045"), worker_id="B").run_once()

    results = {}
    for run_id, store in ((run_a, store_a), (run_b, store_b)):
        run = store.get_run(run_id)
        assert run["status"] == "succeeded"                        # losing is not a crash
        results[run_id] = next(s["result"] for s in run["steps"] if s.get("tool_name") == "book_interview_slot")
    assert results[run_a]["status"] == "booked"
    assert results[run_b]["error"] == "slot_taken"
    holders = PlacementDb(place).conn.execute("SELECT student_id FROM interview_slot WHERE id = 3").fetchall()
    assert [h[0] for h in holders] == [2]


def test_truly_concurrent_claims_have_one_winner(db_files):
    _, place = db_files
    for roll in ("22IT017", "22CS045"):
        PlacementTools(PlacementDb(place)).apply_to_drive(roll, 2)
    version = PlacementDb(place).slot_version(3)
    barrier, wins = threading.Barrier(8), []

    def contender(student_id):
        db = PlacementDb(place)
        barrier.wait()
        wins.append(db.claim_slot(3, student_id, version))

    threads = [threading.Thread(target=contender, args=(1 + i % 2,)) for i in range(8)]
    for t in threads:
        t.start()
    for t in threads:
        t.join()
    assert wins.count(True) == 1 and wins.count(False) == 7
    assert PlacementDb(place).slot_version(3) == version + 1

