# {{ cookiecutter.project_name }}

{{ cookiecutter.project_short_description }}

## Quickstart

Install dependencies:

```
> pip install -r requirements.txt
```

Start Streamlit

```
> streamlit run app.py

  You can now view your Streamlit app in your browser.

  Network URL: http://172.17.0.2:8501
  External URL: http://152.37.119.122:8501

```

Make changes to your app in the `app.py` file inside the "app" folder.

## Run inside Docker image locally (Optional)

You can run the app locally inside Docker to ensure the app will work fine after the deployment.

You need to install Docker on your machine in order to be able to run this command

```
> pollination-apps run app {{ cookiecutter.pollination_owner }} --name "{{ cookiecutter.project_name }}"
```

## Deploy to Pollination

```
> pollination-apps deploy app --name "{{ cookiecutter.project_name }}" --{{ cookiecutter.app_visibility }} --api-token "Your api token from Pollination"
```

{% if cookiecutter.ci == "github-manual" %}

## Configure Github Actions

In order to configure github actions to deploy your app you will need to:

1. [Create](https://docs.github.com/en/get-started/quickstart/create-a-repo) a repository on Github
2. [Add](https://docs.github.com/en/actions/security-guides/encrypted-secrets) a secret called `POLLINATION_TOKEN` with your Pollination API key as the value
3. Create [a new release](https://docs.github.com/en/repositories/releasing-projects-on-github/managing-releases-in-a-repository) of your app on Github with a new tag

Github actions will then package and deploy your code to an app called [{{ cookiecutter.project_name }}](https://app.pollination.cloud/{{ cookiecutter.pollination_owner }}/applications/{{ cookiecutter.project_slug }})

{% endif %}

{% if cookiecutter.ci == "github-automated" %}

## Configure Github Actions

In order to configure github actions to deploy your app you will need to:

1. [Create](https://docs.github.com/en/get-started/quickstart/create-a-repo) a repository on Github
2. [Rename](https://docs.github.com/en/repositories/creating-and-managing-repositories/renaming-a-repository) the repository's main branch to "master"
3. [Add](https://docs.github.com/en/actions/security-guides/encrypted-secrets) a secret called `POLLINATION_TOKEN` with your Pollination API key as the value
4. Create [the first release](https://docs.github.com/en/repositories/releasing-projects-on-github/managing-releases-in-a-repository) of your app on Github with the tag v0.0.0
5. In all your commit messages, use one of the following commit types;

   - `feat`: A new feature
   - `fix`: A bug fix
   - `docs`: Documentation only changes
   - `style`: Changes that do not affect the meaning of the code (white-space, formatting, missing semi-colons, etc)
   - `refactor`: A code change that neither fixes a bug nor adds a feature
   - `perf`: A code change that improves performance or size
   - `test`: Adding missing tests or correcting existing tests
   - `chore`: Other changes that don't modify src/test/
   - `build`: Changes that affect the build system or external dependencies (example: changing the version of a dependency)
   - `ci`: Changes to our CI or CD pipelines

   Examples of commit messages:

   - fix: Remove unused imports
   - feat: Add capability to use analysis period

   **Note** that the commit messages with only `fix` and `feat` type will trigger a deployment to Pollination.

Github actions will then package and deploy your code to an app called [{{ cookiecutter.project_name }}](https://app.pollination.cloud/{{ cookiecutter.pollination_owner }}/applications/{{ cookiecutter.project_slug }})

{% endif %}
