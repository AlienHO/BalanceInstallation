#include <Servo.h>

Servo servo1;    // 创建第一个Servo对象
Servo servo2;    // 创建第二个Servo对象
Servo servo3;    // 创建第三个Servo对象

int dataIndex = 0; // 创建整数型变量，存储输入数据序列号

void setup() {
  servo1.attach(5); // 将第一个伺服电机连接到5号引脚
  servo2.attach(6); // 将第二个伺服电机连接到6号引脚
  servo3.attach(7); // 将第三个伺服电机连接到7号引脚
  
  servo1.write(0); // 设置第一个伺服电机的初始位置为0度
  servo2.write(0); // 设置第二个伺服电机的初始位置为0度
  servo3.write(0); // 设置第三个伺服电机的初始位置为0度

  Serial.begin(9600); // 启动串口通讯，传输波特率9600
  Serial.println("Please input three numbers separated by commas.");
}

void loop() {          
  if (Serial.available() > 0) {  
    dataIndex++;       // 处理数据序列号并通过串口监视器显示
    Serial.print("dataIndex = ");
    Serial.print(dataIndex);
    Serial.print(" , ");      

    int pos1 = Serial.parseInt(); // 解析串口数据中的第一个整数
    int pos2 = Serial.parseInt(); // 解析串口数据中的第二个整数
    int pos3 = Serial.parseInt(); // 解析串口数据中的第三个整数
    
    Serial.print("Set servo positions: ");
    Serial.print(pos1);
    Serial.print(", ");
    Serial.print(pos2);
    Serial.print(", ");
    Serial.println(pos3);

    servo1.write(pos1); // 设置第一个伺服电机的位置
    servo2.write(pos2); // 设置第二个伺服电机的位置
    servo3.write(pos3); // 设置第三个伺服电机的位置

    delay(15);
  }
}
