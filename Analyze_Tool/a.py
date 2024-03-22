x=[2935.0999977588654,1908.1206185817719,1401.791358947754,1142.4294373989105]
y=[128,256,512,1024]
print(" ## Current training time(sec) (128-1024) ## " )
for i,j in zip(x,y):
	print("{0} node: {1}".format(j,i))

print(" ")
print(" ## t+1 / t  ## ")
print("128->256: ", x[1] / x[0])
print("256->512: ",x[2] / x[1])
print("512->1024: ",x[3] / x[2])
print(" --- Expected ----")
print("1024->2048: ",0.89)
print("2048->4096: ",0.97)
print("4096->8192): ",1.05)
print(" ")

print(" ## Training time (128-1024)  + 2048,4096 (expected) ## " )
exp_2048 = 1142.4294373989105 * 0.89 
exp_4096 = exp_2048 * 0.97 
exp_8192 = exp_4096 * 1.05

for i,j in zip(x,y):
	print("{0} node: {1}".format(j,i))
print(" --- Expecetd --- ")
print "2048node: ",exp_2048
print "4096node: ",exp_4096
print "8192node: ",exp_8192

