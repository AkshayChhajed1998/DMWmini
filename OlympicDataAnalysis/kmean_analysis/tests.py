from django.test import TestCase
from django.urls import reverse


class testKMeans(TestCase):

  @classmethod
  def setUpTestData(cls):
    pass

  def test_link_init(self):
    response = self.client.get('/kmeans/init/')
    self.assertEqual(response.status_code, 200)
    self.assertTemplateUsed(response,'kmean_analysis/kmeans.html')

  def test_ajax_call(self):
    response = self.client.post('/kmeans/perform/',{'type':'GDP','year':'2016'})
    self.assertTemplateUsed(response,'kmean_analysis/kmeans.html')
    self.assertContains(response,'id="fig1"')
    self.assertContains(response,'id="fig2"')
  
  """Failing tests
  def test_ajax_call(self):
    response = self.client.post('/kmeans/perform/',{'types':['GDP','GO']})
    self.assertTemplateUsed(response,'kmean_analysis/kmeans.html')
    self.assertContains(response,'id="fig1"')
    self.assertContains(response,'id="fig2"')
  
  def test_link_init(self):
    response = self.client.get('/kmeans/init/')
    self.assertEqual(response.status_code, 200)
    self.assertTemplateUsed(response,'kmean_analysis/kmean.html')
  """ 