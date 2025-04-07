# include <iostream>
# include <vector>
# include <algorithm>
# include <iostream>

// 使用辗转相除法（基本版）
int gcdBasic(int a, int b) {
    if (b == 0) return a; // 如果b为0，则a即为最大公约数
    return gcdBasic(b, a % b); // 递归调用自身，交换参数并使用余数继续计算
}

// 使用更高效的欧几里得算法（标准版）
int gcd(int a, int b) {
    while (b != 0) { // 当b不为零时循环执行
        int temp = b; // 保存当前的b值，即将要更新a的值
        b = a % b; // 更新b为余数
        a = temp;   // 将原来的b赋值给a
    }
    return a; // 返回最大公约数
}

int main() {
    int num1, num2;
    
    // std::cout << "请输入两个整数: ";
    std::cin >> num1 >> num2;

    std::cout << "使用基本版算法计算的最大公约数是：" << gcdBasic(num1, num2) << std::endl;
    std::cout << "使用标准版欧几里得算法计算的最大公约数是：" << gcd(num1, num2) << std::endl;

    return 0;
}






