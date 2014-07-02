import __init__,os,unittest,hashlib
from pedant.screenshots import Worker	


class TestScreenshotFunctions(unittest.TestCase):

	def setUp(self):
		self.testWorker = Worker.Worker( {"FakeBrowser":True} , [], "", "" )
		self.testDir = os.path.dirname( __file__ ) + os.sep + 'testData' + os.sep
		self.tmpDir = self.testDir + 'tmp' + os.sep
		if not os.path.isdir( self.tmpDir ):
			os.makedirs( self.tmpDir )

	def test_fake_pathes(self):
		self.assertEqual( {}, self.testWorker.calculatePathes(), "Pathes must be empty" )

	def test_compare_same(self):
		image_1 = self.testDir + "sameImage.png"
		image_diff = self.tmpDir + "diffImage.png"
		self.assertEqual( False, self.testWorker.compare_screenshots( image_1 , image_1, image_diff) )

	def test_compare_diff(self):
		image_1 = self.testDir + 'differImage1.png'
		image_2 = self.testDir + 'differImage2.png'
		image_diff = self.tmpDir + 'differImage1-2Difference.actual.png'
		self.assertEqual( True, self.testWorker.compare_screenshots( image_1 , image_2, image_diff) )
		exp_diff_image = self.testDir + 'differImage1-2Difference.png'
		#check images equals
		self.assertEqual( 
			hashlib.md5(open(exp_diff_image, 'rb').read()).hexdigest(),
			hashlib.md5(open(image_diff, 'rb').read()).hexdigest(),
			"Difference images not equal")

	def test_compare_differ_size(self):
		image_1 = self.testDir + 'differSizeImage1.png'
		image_2 = self.testDir + 'differSizeImage2.png'
		image_diff = self.tmpDir + 'differSizeImage1-2Difference.actual.png'
		self.assertEqual( True, self.testWorker.compare_screenshots( image_1 , image_2, image_diff) )
		exp_diff_image = self.testDir + 'differSizeImage1-2Difference.png'
		#check images equals
		self.assertEqual( 
			hashlib.md5(open(exp_diff_image, 'rb').read()).hexdigest(),
			hashlib.md5(open(image_diff, 'rb').read()).hexdigest(),
			"Difference images not equal")
		#invert test
		image_diff = self.tmpDir + 'differSizeImage2-1Difference.actual.png'
		self.assertEqual( True, self.testWorker.compare_screenshots( image_2 , image_1, image_diff) )
		exp_diff_image = self.testDir + 'differSizeImage2-1Difference.png'
		#check images equals
		self.assertEqual( 
			hashlib.md5(open(exp_diff_image, 'rb').read()).hexdigest(),
			hashlib.md5(open(image_diff, 'rb').read()).hexdigest(),
			"Difference images not equal")

if __name__ == '__main__':
    unittest.main()