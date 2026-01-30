terraform {
  required_providers {
    github = {
      source  = "integrations/github"
      version = "~> 5.0"
    }
  }
}

provider "github" {
  token = var.github_token
}

resource "github_repository" "example" {
  name        = var.repository_name
  description = var.repository_description
  visibility  = "private"
  auto_init   = true
}

output "repository_url" {
  value       = github_repository.example.html_url
  description = "URL of the created repository"
}