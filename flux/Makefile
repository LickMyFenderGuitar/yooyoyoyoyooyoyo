CXX = g++
CXXFLAGS = -std=c++17 -Wall

SRC = src/main.cpp src/lexer.cpp src/parser.cpp src/runtime.cpp src/system.cpp
OBJ = $(SRC:.cpp=.o)
TARGET = flux

all: $(TARGET)

$(TARGET): $(OBJ)
	$(CXX) $(CXXFLAGS) -o $(TARGET) $(OBJ)

%.o: %.cpp
	$(CXX) $(CXXFLAGS) -c $< -o $@

clean:
	rm -f $(OBJ) $(TARGET)
