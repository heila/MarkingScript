import sys
import memo 
from StringIO import StringIO
import inspect

alternate_dict = {}
alternate_dict['cartesian_to_polar'] = ['cartesian_to_polar','cartesianToPolar','cartesion_to_polar','Polar_Coordinates']
alternate_dict['mercator'] = ['mercator','mercator_projection','mecartor','Mercator','Mercator_projection']
alternate_dict['sort3'] = ['sort3','sort','Sort3']

input_dict = {}
input_dict['cartesian_to_polar'] = [[0,0],[-5,0],[0,7],[1.25,1.25],[-1.75,-2.68]]
input_dict['mercator'] = [[0,0,0],[0,-33.9337,-18.8645],[-33.9337,-33.9337,-18.8645],[23,348.8,360],]
input_dict['sort3'] = [[1,2,3],[1,1,1],[-200,-10,-7236],[3.3,2.2,1.4],[-1,0,1]]



def printError(message):
	print "<div style=\"color:red;\">Exception:</br>", message, "</div>"

def printMethodName(name):
	print "<h3  style=\"color:blue;\">" , name,"</h3>"

def printResults(results):
	print "<p>" , results,"</p>"

def printCode(code):
	print "<pre>" , code,"</pre>"

def find_test_method(test_method):
	for method in dir(test_module): # search for method "method_name" in the test file
		if (method in alternate_dict[test_method]):
			return method
	return None

def printFailTest(inputs, correct, answer):
	print "<div style=\"color:red;\">Fail test: input: ",  str(inputs),  "</div>"
	print "<div> Correct answer: ", str(correct) +  "</div>"
	print "<div> Answer: ", str(answer), "</div>"


def test_approx(test_method):
		method = find_test_method(test_method)
		if (method == None):
			printError("Method not found.")
			printResults(dir(test_module))
			return ""
			
		printCode(inspect.getsource( eval("test_module." + method)))
		
		func_memo = eval("memo." + test_method)
		func_test = eval("test_module." + method)

		num_tests_passed = 0 # counts the number of tests passed
		passed =  True
		
		# run tests
		for i, value in enumerate(input_dict[test_method]):
			try: 
				
				ans_memo = func_memo(*value)
				ans_test = func_test(*value)

				if (len(ans_memo) == len(ans_test)):					
					for c in range(len(ans_memo)):
						if ( not equals_approx(ans_memo[c], ans_test[c])):
							passed = False
							break
				else:
					passed = False

				if (passed):
					num_tests_passed = num_tests_passed+1
				else:
					printFailTest(str(value), str(ans_memo), str(ans_test))
			except Exception, err:                                                                                          
				printError("Test crashed on input: " +  str(value) + " Exception: " + str(err))                                                
				passed = False
		return  str(num_tests_passed)+ "/"+ str(i+1) + " tests passed"



def capture(func, *args, **kwargs):
	capture = StringIO()
	save_stdout = sys.stdout
	sys.stdout = capture
	try:	
		result = func(*args)
	except Exception, err:
		result = str(err)
	sys.stdout = save_stdout
	value = capture.getvalue()	
	return (result, value)


def equals(value1, value2):
	if (value1 == value2):
		return True
	else:
		return False

def equals_approx(value1, value2):
	if(abs(value1 - value2) < 0.00001):
		return True
	else: 
		return False


if __name__ == '__main__':
	try:
		test_module_name = sys.argv[1] #filename of test module
		params = [test_module_name, None, None, alternate_dict.keys(),-1]
		result  = capture(__import__,*params)
		test_module = result[0]
		if ( not isinstance(test_module, str)):
			
			for method in alternate_dict : # vir elke method wat getoets moet word
				try:			
					printMethodName(method)		
					printResults(test_approx(method))
				except Exception, err:
					printError("Error testing method " + method +  ": " + str(err))
		else:
			printError("Error importing module due to " + test_module)
			f = open(test_module_name + ".py",'r')
			print "<pre>"
			for i, value in enumerate(f):
				print i +1, "\t", value,
			print "</pre>"


	except Exception, err:
		printError("Error importing module due to " + str(err))

	
	
