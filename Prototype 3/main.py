#Just the logic no GUI! 
import subprocess
import os

def main():
    base_path = r"C:\Users\mdfah\OneDrive\Desktop\FYP\Prototype 3"  # Replace this with your directory

    while True:
        print("\nSelect a program to run:")
        print("1. Mouse Control")
        print("2. Two Hands Gesture Control")
        print("3. Exit")
        
        choice = input("Enter your choice (1/2/3): ")
        
        if choice == "1":
            print("\nRunning Mouse Control...")
            subprocess.run(["python", os.path.join(base_path, "MouseControl.py")], shell=True)
        elif choice == "2":
            print("\nRunning Two Hands Gesture Control...")
            subprocess.run(["python", os.path.join(base_path, "control_2hands.py")], shell=True)
        elif choice == "3":
            print("\nExiting. Goodbye!")
            break
        else:
            print("Invalid choice. Please try again.")

if __name__ == "__main__":
    main()
