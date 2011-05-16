import unittest
import interface_factory
import api_details

interface = interface_factory.get_adaptive_interface_obj()

class TestAdaptivePayment(unittest.TestCase):

    def test_make_simple_payment(self):
        response = interface.make_simple_payment(
            email=api_details.EMAIL_PERSONAL, amount=10, currency_code='USD',
            cancel_url="http://ebay.com", return_url="http://ebay.com")

        self.assertTrue("payKey" in response.json)
        self.assertEqual(response.paymentExecStatus, "CREATED")
        self.assertEqual(response.responseEnvelope["ack"], "Success")

    def test_get_simple_payment_redirect(self):
        redirect = interface.get_simple_payment_redirect("test")
        self.assertEqual(interface.config.PAYPAL_URL_BASE
                         + "?cmd=_ap-payment&paykey=test", redirect)

    def test_make_chain_payment(self):
        response = interface.make_chain_payment(
            currency_code='USD',
            cancel_url="http://ebay.com",
            return_url="http://ebay.com",
            primary={"email": api_details.EMAIL_PERSONAL, "amount": 20},
            secondary=[{"email": api_details.EMAIL_MERCHANT, "amount": 10}]
        )

        self.assertTrue("payKey" in response.json)
        self.assertEqual(response.paymentExecStatus, "CREATED")
        self.assertEqual(response.responseEnvelope["ack"], "Success")




if __name__ == "__main__":
    unittest.main()
