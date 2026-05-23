resource "aws_instance" "example05112026" {
    ami = "ami-0cf0e376c672104d6"
    instance_type = "t3.micro"
    tags = {
        Name = "ExampleInstance05112026"
    }
} 

