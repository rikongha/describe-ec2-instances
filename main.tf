terraform {
    required_version = ">= 0.15"

    required_providers {
        aws = {
            source  = "hashicorp/aws"
            version = "~> 4.0"
        }
    }
}

provider "aws" {
    profile = "cocus"
    region = "eu-central-1"
}