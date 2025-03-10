def calculate_rectangle_area():
    # Get input from user
    length = float(input("Enter the length of the rectangle: "))
    width = float(input("Enter the width of the rectangle: "))
    
    # Calculate area
    area = length * width
    
    # Display the result with input values
    print(f"\nWith length {length} and width {width}")
    print(f"The area of the rectangle is: {area} square units")

# Run the program
if __name__ == "__main__":
    print("Rectangle Area Calculator")
    print("-----------------------")
    calculate_rectangle_area()

