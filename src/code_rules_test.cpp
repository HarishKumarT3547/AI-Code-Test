#include <iostream>
#include <string>
#include <vector>
#include <memory>
#include <stdexcept>
#include <gtest/gtest.h>

// Good Practice: Use namespaces to avoid naming conflicts
namespace code_rules_test {

// Good Practice: Use constexpr for compile-time constants
constexpr int MAX_SIZE = 100;
constexpr double PI = 3.14159;

// Good Practice: Use enum class for type-safe enumerations
enum class Status {
    SUCCESS,
    FAILURE,
    PENDING
};

// Good Practice: Use struct for data-only types
struct Point {
    double x;
    double y;
};

// Good Practice: Use class for types with behavior
class Circle {
public:
    // Good Practice: Use explicit for single-argument constructors
    explicit Circle(double radius) : radius_(radius) {
        if (radius <= 0) {
            throw std::invalid_argument("Radius must be positive");
        }
    }

    // Good Practice: Use const member functions
    double getArea() const {
        return PI * radius_ * radius_;
    }

    // Good Practice: Use noexcept when appropriate
    double getRadius() const noexcept {
        return radius_;
    }

private:
    // Good Practice: Use trailing underscore for member variables
    double radius_;
};

// Good Practice: Use smart pointers for resource management
class ResourceManager {
public:
    ResourceManager() : data_(std::make_unique<std::vector<int>>()) {}

    // Good Practice: Use move semantics
    void addData(std::vector<int>&& data) {
        if (data.size() > MAX_SIZE) {
            throw std::length_error("Data size exceeds maximum");
        }
        *data_ = std::move(data);
    }

    // Good Practice: Use const reference for read-only parameters
    const std::vector<int>& getData() const {
        return *data_;
    }

private:
    std::unique_ptr<std::vector<int>> data_;
};

// Bad Practice Examples (commented out but kept for reference)
/*
// Bad Practice: Using magic numbers
double calculateArea(double radius) {
    return 3.14159 * radius * radius;  // Magic number
}

// Bad Practice: Raw pointer usage
int* createArray(int size) {
    return new int[size];  // Potential memory leak
}

// Bad Practice: No error handling
double divide(double a, double b) {
    return a / b;  // No check for division by zero
}
*/

// Test Cases
TEST(CodeRulesTest, CircleAreaCalculation) {
    Circle circle(5.0);
    EXPECT_DOUBLE_EQ(circle.getArea(), 78.53975);
}

TEST(CodeRulesTest, CircleInvalidRadius) {
    EXPECT_THROW(Circle(-1.0), std::invalid_argument);
}

TEST(CodeRulesTest, ResourceManagerDataHandling) {
    ResourceManager manager;
    std::vector<int> data = {1, 2, 3, 4, 5};
    manager.addData(std::move(data));
    EXPECT_EQ(manager.getData().size(), 5);
}

TEST(CodeRulesTest, ResourceManagerSizeLimit) {
    ResourceManager manager;
    std::vector<int> largeData(MAX_SIZE + 1);
    EXPECT_THROW(manager.addData(std::move(largeData)), std::length_error);
}

} // namespace code_rules_test

int main(int argc, char** argv) {
    testing::InitGoogleTest(&argc, argv);
    return RUN_ALL_TESTS();
} 