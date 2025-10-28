from django.test import TestCase
from unittest.mock import patch


from django.test import TestCase
from django.utils import timezone

from library.models import Author, Loan, Book, Member, User

from library.tasks import check_overdue_loans

from datetime import timedelta


class CheckOverdueLoansTaskTest(TestCase):
	def setUp(self):
		author =Author.objects.create(first_name="User1", last_name="ONe")


		user1 = User.objects.create_user(username="john", email="johndoe@gmail.com",password="pass")

		member1 = Member.objects.create(user=user1) 

		b1 = Book.objects.create(
			title="Book one", 
			author=author, isbn='1030303503010', 
			genre="fiction",
			available_copies=32323
		)
		today = timezone.now().date()
		past =today - timedelta(days=2)

		Loan.objects.create(book=b1, member=member1,due_date=past,is_returned=False)


	@patch("library.tasks.send_mail")
	def test_check_overdue_loans_sends_email(self, mock_send_mail):
		check_overdue_loans()

		assert mock_send_mail.call_count==1
		_, kwargs = mock_send_mail.call_args
		assert kwargs["recipient_list"]==["johndoe@gmail.com"]



# Create your tests here.
