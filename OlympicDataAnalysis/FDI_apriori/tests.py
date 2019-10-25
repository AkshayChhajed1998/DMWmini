from django.test import TestCase
from django.urls import reverse


class testApriori(TestCase):

  @classmethod
  def setUpTestData(cls):
    pass

  def test_link_init(self):
    response = self.client.get('/fiapriori/init/')
    self.assertEqual(response.status_code, 200)
    self.assertTemplateUsed(response,'FDI_apriori/apriori.html')

  def test_ajax_call(self):
    response = self.client.post('/fiapriori/perform/',{'sport':'Football'})
    self.assertContains(response,'id="table"',count=1)
    self.assertContains(response, 'class="dataframe ui celled striped selectable inverted purple table"')


  """Failing Test
  def test_link_init(self):
    response = self.client.get('/fiapriori/init/')
    self.assertEqual(response.status_code, 200)
    self.assertTemplateUsed(response,'FDI_apriori/aprioris.html')

  def test_ajax_call(self):
    response = self.client.post('/fiapriori/perform/',{'Sport':['Football','Judo']})
    self.assertContains(response,'id="table"',count=1)
    self.assertContains(response, 'class="dataframe ui celled striped selectable inverted purple table"')
  """