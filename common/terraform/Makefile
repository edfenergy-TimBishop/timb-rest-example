.PHONY: all
TERRAFORM_PROVIDER := "$(or $(env),${env},dev)"

all: init plan apply plan-with-exit-code

init:
	$(call stdout, "Removing cached terraform modules.")
	@rm -Rf .terraform/modules
	$(call stdout, "Initialiasing terraform.")
	@terraform init -reconfigure
	$(call stdout, "Validating terraform code.")
	@echo "Validating terraform code."
	@terraform validate -no-color

plan:
	$(call stdout, "Running a terraform plan")
	@terraform plan -no-color -refresh=true 

apply:
	$(call stdout, "Deploying the infrastructure.")
	@terraform apply -no-color -auto-approve

plan-with-exit-code:
	$(call stdout, "Validating the deployment")
	@terraform plan -no-color -refresh=true -detailed-exitcode
	$(call stdout, "Deployment is completed.")

define stdout
	@tput setaf 3
	@echo $1
	@tput sgr0
endef
