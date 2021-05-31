class Sample():
    def __enter__(self):
        print('=====in enter')
        return self
        
    def __exit__(self, exc_type, exc_val, exc_tb):
        print ("=====type: " + str(exc_type))
        print ("======val: "+ str( exc_val))
        print ("========tb: "+ str( exc_tb))


with Sample() as sample:
    raise Exception("运行代码块出现错误")

print("run end")