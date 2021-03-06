# design_project
Our health tracker/diet planning website app aims to aid consumers with making health-conscious decisions and empower them to follow through on these commitments. We intend to do this by providing consumers a simple and easy-to-use application that will help them find food, exercises, and recipes based on diet and health expectations. Given recent increasing consumer interest in living healthy and mindful lives, we believe that providing consumers with the ability to track, manage, as well as discover new diets will help solve real-world health and diet misinformation as well as issues stemming from the lack of information about healthy foods. 


Master is production and should only receive merges with --squash. It is located at https://design-project-b23.herokuapp.com/

Develop is a utility to check if deployments will succeed on master- it should also only recieve merges with --squash. It is located at https://design-project-b23-dev.herokuapp.com/

# Vagrant
Install virtualbox and vagrant on your machine (prerequisites)
- Run `vagrant up` in the root directory of this project: This will build your
  development environment and may take more than 20 minutes. Do not shut your
  computer off during this time.
- When the development environment is created, you can enter the environment
  using ssh by the function `vagrant ssh`, once again called in the root
  directory of the project

## Utilities included
    - Functional docker installation
    - Heroku cli client
    - Pipenv installation
    - Installation of `magic-wormhole` (a peer-to-peer file transfer utility)
    - Connection to project specific VPN
## Utilities currently not included
    - Desktop environment (xfce)
    - Any kind of IDE (visual studio)
    - Any kind of web browser (firefox)
