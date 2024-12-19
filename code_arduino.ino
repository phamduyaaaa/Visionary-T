#include <Servo.h>  // Thêm thư viện Servo

Servo myServo;  // Tạo đối tượng Servo
void setup() {
  // Khởi tạo giao tiếp nối tiếp với tốc độ 9600 bps
  Serial.begin(9600);  // Cấu hình tốc độ truyền dữ liệu (9600 bps)
  
  // Kết nối servo với chân PWM 9
  myServo.attach(9);
  
  // Quay servo về vị trí 120 độ ban đầu
 
  // In thông báo khi servo ở 120 độ
}

void loop() {

  // Kiểm tra xem có dữ liệu gửi từ máy tính không
  if (Serial.available() > 0) {
    int value = Serial.read();  // Đọc giá trị nhận được từ máy tính

    // Kiểm tra giá trị nhận được và điều khiển servo
    if (value == '1') {
      myServo.write(65);  // Quay servo đến góc 65 độ
      Serial.println("Servo quay đến 65 độ");  // In ra thông báo
    } else if (value == '0') {
      myServo.write(120);  // Quay servo đến góc 120 độ
      Serial.println("Servo quay đến 120 độ");  // In ra thông báo
    } else {
      Serial.println("Giá trị không hợp lệ, vui lòng gửi '0' hoặc '1'");
    }
  }
}
