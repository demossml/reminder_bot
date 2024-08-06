import unittest
from unittest.mock import patch, MagicMock, call
from datetime import datetime
import schedule
import logging
from bd.model import Chat, Post

from schedules.__init__ import schedule_messages, job


# Настройка логирования
logging.basicConfig(
    level=logging.DEBUG, format="%(asctime)s - %(levelname)s - %(message)s"
)


class TestScheduler(unittest.TestCase):

    @patch("bd.model.Post.objects")
    @patch("schedule.every")
    def test_schedule_messages(self, mock_every, mock_post_objects):
        # Mock data to return when Post.objects() is called
        mock_post_objects.return_value = [
            {
                "chat_name": "Chat1",
                "text": "Hello, Chat1!",
                "month": "08",
                "day_of_month": "01",
                "time": "10:00",
            },
            {
                "chat_name": "Chat2",
                "text": "Hello, Chat2!",
                "day_of_month": "02",
                "time": "10:30",
            },
        ]

        # Call the function to be tested
        schedule_messages()

        # Ensure that schedule.every().day.at().do() is called with correct arguments
        self.assertEqual(mock_every.return_value.at.return_value.do.call_count, 2)

        # Verify the first scheduled job
        mock_every.return_value.at.assert_any_call("10:00")
        mock_every.return_value.at.assert_any_call("10:30")

    @patch("bd.model.Post.objects")
    @patch("datetime.datetime")
    @patch("schedule.every")
    def test_monthly_job(self, mock_every, mock_datetime, mock_post_objects):
        # Mock current date to match the scheduling day
        mock_datetime.today.return_value = datetime(2024, 8, 1)
        mock_datetime.side_effect = lambda *args, **kw: datetime(*args, **kw)

        mock_post_objects.return_value = [
            {
                "chat_name": "Chat2",
                "text": "Hello, Chat2!",
                "day_of_month": "01",
                "time": "10:30",
            }
        ]

        # Call the function to be tested
        schedule_messages()

        # Run the scheduled jobs
        schedule.run_all()

        # Ensure job function was called
        with patch("builtins.print") as mocked_print:
            job("Chat2", "Hello, Chat2!")
            mocked_print.assert_called_with("Chat2")


if __name__ == "__main__":
    unittest.main()
