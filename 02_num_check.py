def num_check():
   
    while True:
        try:
            response = int(input("Enter a number: "))
            # continues fine
            

        except ValueError:
            print("Bad input")
        
        break



num_check()
        