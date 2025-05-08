import unittest
from ps5 import NewsStory, Trigger, PhraseTrigger, TitleTrigger, DescriptionTrigger, TimeTrigger, BeforeTrigger, AfterTrigger
from datetime import datetime
import pytz

class TestNewsStory(unittest.TestCase):
    def test_news_story_creation(self):
        pub_date = datetime(2025, 5, 6, 10, 0, 0, tzinfo=pytz.utc)
        story = NewsStory("guid123", "Test Title", "Test Description", "http://example.com", pub_date)
        self.assertEqual(story.get_guid(), "guid123")
        self.assertEqual(story.get_title(), "Test Title")
        self.assertEqual(story.get_description(), "Test Description")
        self.assertEqual(story.get_link(), "http://example.com")
        self.assertEqual(story.get_pubdate(), pub_date)

class TestPhraseTrigger(unittest.TestCase):
    def test_is_phrase_in_case_insensitive(self):
        trigger = PhraseTrigger("intel")
        self.assertTrue(trigger.is_phrase_in("This article discusses Intel processors."))
        self.assertTrue(trigger.is_phrase_in("The INTEL company announced new products."))
        self.assertTrue(trigger.is_phrase_in("intel"))
        self.assertFalse(trigger.is_phrase_in("This has nothing to do with AMD."))

    def test_is_phrase_in_whole_phrase(self):
        trigger = PhraseTrigger("new york")
        self.assertTrue(trigger.is_phrase_in("I visited New York City."))
        self.assertFalse(trigger.is_phrase_in("This is a new way to work."))
        self.assertFalse(trigger.is_phrase_in("The York company is expanding."))

class TestTitleTrigger(unittest.TestCase):
    def test_evaluate_title_case_insensitive(self):
        now = datetime.now(pytz.utc)
        story1 = NewsStory("guid1", "Intel Announces New Chip", "...", "http://example.com/1", now)
        story2 = NewsStory("New INTEL Processor Launched", "...", "...", "http://example.com/2", now)
        story3 = NewsStory("AMD Releases Updated CPU", "...", "...", "http://example.com/3", now)
        trigger = TitleTrigger("intel")
        self.assertTrue(trigger.evaluate(story1))
        self.assertTrue(trigger.evaluate(story2))
        self.assertFalse(trigger.evaluate(story3))

    def test_evaluate_title_whole_phrase(self):
        now = datetime.now(pytz.utc)
        story1 = NewsStory("New York City News", "...", "...", "http://example.com/4", now)
        story2 = NewsStory("New things are happening in York", "...", "...", "http://example.com/5", now)
        trigger = TitleTrigger("New York")
        self.assertTrue(trigger.evaluate(story1))
        self.assertFalse(trigger.evaluate(story2))

class TestDescriptionTrigger(unittest.TestCase):
    def test_evaluate_description(self):
        now = datetime.now(pytz.utc)
        story1 = NewsStory("guid1", "...", "The company Intel released a new product.", "http://example.com/1", now)
        story2 = NewsStory("...", "...", "New processor from INTEL is faster.", "http://example.com/2", now)
        story3 = NewsStory("...", "...", "AMD's latest offering shows strong performance.", "http://example.com/3", now)
        trigger = DescriptionTrigger("intel")
        self.assertTrue(trigger.evaluate(story1))
        self.assertTrue(trigger.evaluate(story2))
        self.assertFalse(trigger.evaluate(story3))

class TestTimeTrigger(unittest.TestCase):
    def test_time_trigger_creation(self):
        time_str = "05 May 2025 10:30:00"
        trigger = TimeTrigger(time_str)
        expected_time = datetime(2025, 5, 5, 10, 30, 0, tzinfo=pytz.timezone("EST"))
        self.assertEqual(trigger.time, expected_time)

    def test_invalid_time_format(self):
        with self.assertRaises(ValueError):
            TimeTrigger("invalid time")

class TestBeforeAfterTrigger(unittest.TestCase):
    def setUp(self):
        self.est_tz = pytz.timezone("EST")
        self.utc_tz = pytz.utc
        self.ref_time_str = "06 May 2025 12:00:00"
        self.ref_time = datetime.strptime(self.ref_time_str + " EST", "%d %b %Y %H:%M:%S %Z")

    def test_before_trigger(self):
        before_trigger = BeforeTrigger(self.ref_time_str)
        story_before = NewsStory("id1", "...", "...", "...", self.est_tz.localize(datetime(2025, 5, 6, 10, 0, 0)))
        story_after = NewsStory("id2", "...", "...", "...", self.est_tz.localize(datetime(2025, 5, 6, 14, 0, 0)))
        self.assertTrue(before_trigger.evaluate(story_before))
        self.assertFalse(before_trigger.evaluate(story_after))

    def test_after_trigger(self):
        after_trigger = AfterTrigger(self.ref_time_str)
        story_before = NewsStory("id1", "...", "...", "...", self.est_tz.localize(datetime(2025, 5, 6, 10, 0, 0)))
        story_after = NewsStory("id2", "...", "...", "...", self.est_tz.localize(datetime(2025, 5, 6, 14, 0, 0)))
        self.assertFalse(after_trigger.evaluate(story_before))
        self.assertTrue(after_trigger.evaluate(story_after))

    def test_time_trigger_with_utc_story(self):
        before_trigger = BeforeTrigger("06 May 2025 12:00:00")
        after_trigger = AfterTrigger("06 May 2025 12:00:00")
        story_utc_before = NewsStory("id3", "...", "...", "...", self.utc_tz.localize(datetime(2025, 5, 6, 9, 0, 0))) # 9 UTC is 4 EST
        story_utc_after = NewsStory("id4", "...", "...", "...", self.utc_tz.localize(datetime(2025, 5, 6, 17, 0, 0))) # 17 UTC is 12 EST
        self.assertTrue(before_trigger.evaluate(story_utc_before))
        self.assertFalse(before_trigger.evaluate(story_utc_after))
        self.assertFalse(after_trigger.evaluate(story_utc_before))
        self.assertTrue(after_trigger.evaluate(story_utc_after))

if __name__ == '__main__':
    unittest.main()