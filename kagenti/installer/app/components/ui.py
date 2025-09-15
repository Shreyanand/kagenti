# Assisted by watsonx Code Assistant
# Copyright 2025 IBM Corp.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

import typer

from .. import config
from ..utils import console, run_command


def install(**kwargs):
    """Installs the Kagenti UI from its deployment YAML."""
    run_command(
        [
            "kubectl",
            "apply",
            "-n",
            "kagenti-system",
            "-f",
            str(config.RESOURCES_DIR / "global-environments.yaml"),
        ],
        f"Applying global-environments configmap in 'kagenti-system'",
    )
    # Create the auth secret, containing the Keycloak client secret
    run_command(
        [
            "kubectl",
            "replace", # Use replace --force to ensure the job gets replaced
            "--force",
            "-f",
            str(config.RESOURCES_DIR / "ui-oauth-secret.yaml"),
        ],
        "Creating OAuth secret",
    )
    run_command(
        [
            "kubectl",
            "wait",
            "--for=condition=complete",
            "job/kagenti-ui-oauth-job",
            "-n", "kagenti-system",
            "--timeout=300s",
        ],
        "Waiting for auth secret job to complete",
    )
    ui_yaml_path = config.PROJECT_ROOT / "deployments" / "ui" / "kagenti-ui.yaml"
    if not ui_yaml_path.exists():
        console.log(
            f"[bold red]✗ UI deployment file not found at expected path: {ui_yaml_path}[/bold red]"
        )
        raise typer.Exit(1)

    run_command(["kubectl", "apply", "-f", str(ui_yaml_path)], "Installing Kagenti UI")
    run_command(
        [
            "kubectl",
            "label",
            "ns",
            "kagenti-system",
            "shared-gateway-access=true",
            "--overwrite",
        ],
        "Sharing gateway access for UI",
    )
    run_command(
        [
            "kubectl",
            "rollout",
            "status",
            "-n",
            "kagenti-system",
            "deployment/kagenti-ui",
        ],
        "Waiting for kagenti-ui rollout",
    )
