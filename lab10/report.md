# Infrastructure as Code using Terraform

## Prerequisits
- aws CLI working:
![alt text](image.png)
![alt text](image-1.png)

- GitHub Personal Access Token (PAT) for Terraform (never publish it! - add to .gitignore if written to file)

## GitHub repository IaC setup

- define `variables.tf` and `main.tf` files

- Export GitHub token as an environment variable: `export TF_VAR_github_token=github_token_here`

![](image-2.png)
![alt text](image-3.png)
![alt text](image-4.png)

after `terraform apply`:
![alt text](image-5.png)

- repo successfully created:
![alt text](image-6.png)

- then deleted with `terraform destroy`


## Exercse 1
Refactored files in `/GitHub-repo-refactor.

