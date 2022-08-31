locals {
  dependency_zip = "package/python.zip"
  lambda_zip = "package/describe_ec2_lambda.zip"
}

data "archive_file" "lambda_dependency" {
  type = "zip"
  source_dir = "venv/lib/python3.9/site-packages"
  output_path = local.dependency_zip
}

data "archive_file" "lambda_list" {
  type = "zip"
  source_file = "list.py"
  output_path = local.lambda_zip
}

resource "aws_lambda_layer_version" "lambda_layer" {
  filename   = data.archive_file.lambda_dependency.output_path
  layer_name = "lambda_layer_python"
  compatible_runtimes = ["python3.9"]
  source_code_hash = data.archive_file.lambda_dependency.output_base64sha256
}

resource "aws_lambda_function" "ec2_lambda" {
    filename = data.archive_file.lambda_list.output_path
    function_name = "list"
    role = aws_iam_role.lambda_role.arn
    runtime = "python3.9"
    handler = "list.lambda_handler"
    source_code_hash = data.archive_file.lambda_list.output_base64sha256
}