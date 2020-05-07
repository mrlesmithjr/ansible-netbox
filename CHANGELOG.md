commit 63888d98619f8dc6ee618baa726d9b35399b4af7
Author: Larry Smith Jr <mrlesmithjr@gmail.com>
Date:   Thu May 7 15:43:21 2020 -0400

    Disabled Debian9/Ubuntu16.04 testing

commit f39be44da62466f6b4757d4d3efed6d39c86815b
Author: Larry Smith Jr <mrlesmithjr@gmail.com>
Date:   Thu May 7 12:44:21 2020 -0400

    Added missing exposed ports

commit d9d6926dd85b0900848fffe7e1ba581c655e2d13
Author: Larry Smith Jr <mrlesmithjr@gmail.com>
Date:   Thu May 7 12:32:52 2020 -0400

    Updated Python requirements

commit 9ad0f5f0080e9a6e43073264f749fb4640b4fe6b
Author: Larry Smith Jr <mrlesmithjr@gmail.com>
Date:   Thu May 7 12:32:40 2020 -0400

    Fixed linting issue

commit 2d813a2426a57f658db4e86b8a932b5bb4fd06bf
Author: Larry Smith Jr <mrlesmithjr@gmail.com>
Date:   Thu May 7 12:24:33 2020 -0400

    UGGGG!!!! SO, SO many changes
    
    - Cleaned up linting issues
    - Added real testing for custom modules
    - Updated Netbox version
    - Updated configuration to account for new Netbox version
    - etc, etc

commit a7a773b883dea207800a6b97fe2ff21dbf73404a
Author: Larry Smith Jr <mrlesmithjr@gmail.com>
Date:   Tue Feb 18 16:51:43 2020 -0500

    Added missing required Redis role

commit 2d01ef60449770db0286b8d11a19ff3c77439fb2
Author: Larry Smith Jr <mrlesmithjr@gmail.com>
Date:   Fri Feb 7 16:30:50 2020 -0500

    Lingering changes

commit d5b1c04d277f29ce9bfeb1087d173560a3541b09
Author: Larry Smith Jr <mrlesmithjr@gmail.com>
Date:   Wed Aug 28 23:56:10 2019 -0400

    Added module to add IPAM role(s)

commit 93cb5aeb8f5d5bbfc05078f9f91c791bb8e44014
Author: Larry Smith Jr <mrlesmithjr@gmail.com>
Date:   Wed Aug 28 21:26:16 2019 -0400

    Renamed roles to ipam roles

commit 2cf1c730c8b46c27abd76dc0a2fb46fb398967d9
Author: Larry Smith Jr <mrlesmithjr@gmail.com>
Date:   Wed Aug 28 17:27:19 2019 -0400

    Added roles and vlan groups

commit 302ef80b177059035ee99ee3b82dcb3184e33a78
Author: Larry Smith Jr <mrlesmithjr@gmail.com>
Date:   Wed Aug 28 16:22:16 2019 -0400

    Added VLAN group module

commit a9432f8ee54a83183073947809905e71c372282d
Author: Larry Smith Jr <mrlesmithjr@gmail.com>
Date:   Fri Aug 23 15:53:52 2019 -0400

    Added inital prefixes and devices

commit 3d0ff0706f299c33fd0cad932a60e48e084b784f
Author: Larry Smith Jr <mrlesmithjr@gmail.com>
Date:   Fri Aug 23 08:59:23 2019 -0400

    Added rirs and aggregates

commit 372e7afaa4aa6a09855d52e43387dd06a3063b70
Author: Larry Smith Jr <mrlesmithjr@gmail.com>
Date:   Thu Aug 22 22:13:00 2019 -0400

    Added ability to ingest vlans

commit 471e9d23ff2edc571c9c254b4a2df6a107f15edd
Author: Larry Smith Jr <mrlesmithjr@gmail.com>
Date:   Thu Aug 22 21:50:25 2019 -0400

    Added module to manage VRFs

commit c5f19e1f733d7f937f40ddd757dd100f7cd08444
Author: Larry Smith Jr <mrlesmithjr@gmail.com>
Date:   Thu Aug 22 16:13:57 2019 -0400

    Added ability to ingest VRFs

commit 30ab8882ec1e57248f50e8887f4333538ab7b260
Author: Larry Smith Jr <mrlesmithjr@gmail.com>
Date:   Thu Aug 22 14:43:50 2019 -0400

    Added ingestion script to collect existing data

commit a6ebbf10a90c3ae9fd365f3bc1cce24f91ee5b92
Author: Larry Smith Jr <mrlesmithjr@gmail.com>
Date:   Thu Aug 22 12:30:48 2019 -0400

    Added sites custom module

commit b5a4f0baada73ed59bcb2b857495a0d871f349e9
Author: Larry Smith Jr <mrlesmithjr@gmail.com>
Date:   Thu Aug 22 12:25:56 2019 -0400

    Module tweaks
    
    - Added no_log for token to ensure this is not logged anywhere
    - Added module failure logic

commit 018f9cae5c12c5f51b299db070d68ade6ac85555
Author: Larry Smith Jr <mrlesmithjr@gmail.com>
Date:   Thu Aug 22 00:17:52 2019 -0400

    Changed logic to check for present/existing/etc.

commit 76ed3851bff0d9798c19aba11f6d808dc525a3e2
Author: Larry Smith Jr <mrlesmithjr@gmail.com>
Date:   Wed Aug 21 16:41:07 2019 -0400

    Simplified slug creation
    
    - Added function to account for slug creation

commit 31deaf6b2e3d63807fdc6da4b827d0ea433c497e
Author: Larry Smith Jr <mrlesmithjr@gmail.com>
Date:   Wed Aug 21 16:29:43 2019 -0400

    Added custom module to manage regions

commit 37cb0e31b4745d3f98b909a4f102ccf1234f97c6
Author: Larry Smith Jr <mrlesmithjr@gmail.com>
Date:   Wed Aug 21 15:52:51 2019 -0400

    NetBox configuration updated to latest and params added to reflect

commit 0a1c18fa8bd33b97dea062b1e91304eb55d02869
Author: Larry Smith Jr <mrlesmithjr@gmail.com>
Date:   Wed Aug 21 15:52:06 2019 -0400

    Redis server role removed - Redis now a pre-req

commit b6e186f8ad89ada40873b5ebc19f396219546d26
Author: Larry Smith Jr <mrlesmithjr@gmail.com>
Date:   Wed Aug 21 00:52:41 2019 -0400

    Renamed nbox_tags module to nbox_tag

commit d6f78bc552d00e9cb121dbfe0574f506e1f53c62
Author: Larry Smith Jr <mrlesmithjr@gmail.com>
Date:   Wed Aug 21 00:49:33 2019 -0400

    Changed double quotes to single for consistency

commit da889cc4f2933ed16b89e4ffbd76c8c461d4f106
Author: Larry Smith Jr <mrlesmithjr@gmail.com>
Date:   Tue Aug 20 19:55:37 2019 -0400

    Added module for managing tags

commit ef251e8cdb23f67115f5b2eb88e0a32848926e41
Author: Larry Smith Jr <mrlesmithjr@gmail.com>
Date:   Tue Aug 20 19:55:37 2019 -0400

    Added module for managing tags

commit 28a7d776b02c8370c0b08a6809a8cc30973dd2a5
Author: Larry Smith Jr <mrlesmithjr@gmail.com>
Date:   Tue Aug 20 16:23:56 2019 -0400

    First commit of custom modules
    
    The following custom modules have been added:
    - nbox_tenant_group - Manage tenant group(s)
    - nbox_tenant - Manage tenant(s)

commit a1dc361db8806dfac4ed8bdb1a9ecd9cb73aa564
Author: Larry Smith Jr <mrlesmithjr@gmail.com>
Date:   Sat Feb 22 01:08:11 2020 -0500

    Added Ansible role requirement ansible-bootstrap-python

commit 33bbbc18259c5d81d494cf6c2fdcdf1e48d00d2a
Author: Larry Smith Jr <mrlesmithjr@gmail.com>
Date:   Sat Feb 22 00:45:48 2020 -0500

    Disabled CentOS/Fedora
    
    - Not supported as of yet

commit 7ee81b7acff118b0860c07bf403465c0ab8b9a92
Author: Larry Smith Jr <mrlesmithjr@gmail.com>
Date:   Fri Feb 21 23:58:47 2020 -0500

    Fixed Ansible lint issue

commit a235297e54b5d022c40eab91ec1da8727f4fd7ad
Author: Larry Smith Jr <mrlesmithjr@gmail.com>
Date:   Fri Feb 21 23:50:45 2020 -0500

    Fixing galaxy dependecies

commit 9c599423d3fba56e46877479e87409b5d5243942
Author: Larry Smith Jr <mrlesmithjr@gmail.com>
Date:   Fri Feb 21 23:48:00 2020 -0500

    Changed Molecule scenarios, tests, etc.

commit 9e238082645a3b9f463f1434d0ea24402025e4c5
Author: Larry Smith Jr <mrlesmithjr@gmail.com>
Date:   Fri Feb 21 23:47:46 2020 -0500

    Updated files, etc. after new structure

commit 5d392bd359f0571573268d2ccc0f1196110994ec
Author: Larry Smith Jr <mrlesmithjr@gmail.com>
Date:   Tue Feb 18 16:39:41 2020 -0500

    Added CI badges
    
    - I forgot the badges for CI (Travis, GitHub Actions)

commit 3be34e2e12254fbc9608011322f9049f49aab768
Author: Larry Smith Jr <mrlesmithjr@gmail.com>
Date:   Mon Feb 17 11:16:50 2020 -0500

    Updated Molecule test images

commit ef9f76a8afe3edc4e72a98c4878a711ce22699a8
Author: Larry Smith Jr <mrlesmithjr@gmail.com>
Date:   Mon Feb 17 01:00:29 2020 -0500

    Fixed Ubuntu 18.04 systemd issues
    
    - Switched to different Docker image w/systemd

commit 41f5b1e3bdebf79398fab81e6d868dab984b0967
Author: Larry Smith Jr <mrlesmithjr@gmail.com>
Date:   Sun Feb 16 23:26:21 2020 -0500

    Ubuntu Bionic failing because of systemd (I Think)

commit 0214806f6d3b48b81096f5005c28d1161fd2ae3c
Author: Larry Smith Jr <mrlesmithjr@gmail.com>
Date:   Sun Feb 16 23:11:08 2020 -0500

    Fixed Ansible lint and Ubuntu Xenial testing

commit 03abd31e4dd34caccb3459261f44e86cd562668f
Author: Larry Smith Jr <mrlesmithjr@gmail.com>
Date:   Sun Feb 16 23:10:45 2020 -0500

    Added Ubuntu Xenial as supported

commit 5e95a336958fd8182025a1c3a0830a56dc83f929
Author: Larry Smith Jr <mrlesmithjr@gmail.com>
Date:   Sun Feb 16 22:42:33 2020 -0500

    Remaining new files from cookiecutter template added

commit 1b383354ed2bf510dc35f9599437c02c969c8ce4
Author: Larry Smith Jr <mrlesmithjr@gmail.com>
Date:   Sun Feb 16 22:41:48 2020 -0500

    Added symlinks for requirements.yml
    
    - To ensure that the additional roles are tested with Molecule

commit 0f8f5aa2fa8403cf570e6793342eae8a251a7489
Author: Larry Smith Jr <mrlesmithjr@gmail.com>
Date:   Sun Feb 16 22:41:21 2020 -0500

    Added CI for GitHub/GitLab

commit 1ded8d462216b7c18309e56b47a30bc0092c4ed7
Author: Larry Smith Jr <mrlesmithjr@gmail.com>
Date:   Sun Feb 16 22:40:06 2020 -0500

    Updated license from cookiecutter template

commit 8c80a7a5995af9e628a9e52cdecc1ffd3aaac47b
Author: Larry Smith Jr <mrlesmithjr@gmail.com>
Date:   Sun Feb 16 22:38:59 2020 -0500

    Updates from cookiecutter template
    
    - These updates are from implementing the cookiecutter template.

commit 99bad34d967fc4aa22e1689c4bb5ff7f8c9f033c
Author: Larry Smith Jr <mrlesmithjr@gmail.com>
Date:   Sun Feb 16 22:25:58 2020 -0500

    Replaced old molecule testing

commit c2c99fd9e024b19ff4ae0ce4fb9d5d0b4cf1dbad
Author: Larry Smith Jr <mrlesmithjr@gmail.com>
Date:   Mon Aug 19 16:19:00 2019 -0400

    Fixed missing Ansible required roles

commit b6a1b2ffc813f990eea30ccfc51a9ab9a669a09e
Author: Larry Smith Jr <mrlesmithjr@gmail.com>
Date:   Mon Aug 19 16:07:36 2019 -0400

    Implemented Molecule testing for Vagrant
    
    Had to fix become_user functionality to allow SSH Pipelining.

commit 8a112b79a32a9e53eda357bb4a072475d5b37964
Author: Larry Smith Jr <mrlesmithjr@gmail.com>
Date:   Mon Aug 19 14:22:26 2019 -0400

    Disabled Redis role for now

commit 580e2f010cddb1c604c161f7c275e9b598c8c30f
Author: Larry Smith Jr <mrlesmithjr@gmail.com>
Date:   Mon Aug 19 13:55:52 2019 -0400

    Fixed permissions issue for idempotency

commit d6d611383adbfdaed5c3b6004e32fda0ade07356
Author: Larry Smith Jr <mrlesmithjr@gmail.com>
Date:   Mon Aug 19 08:53:38 2019 -0400

    Updated example playbook

commit 51ecdf7afa642b15df0bcb33c09fd2d4ebec2ac0
Author: Larry Smith Jr <mrlesmithjr@gmail.com>
Date:   Mon Aug 19 08:39:54 2019 -0400

    Resolved linting issues

commit 6b3d3b921c9cc40dd28044cea45cc80bc42ad2f2
Author: Larry Smith Jr <mrlesmithjr@gmail.com>
Date:   Mon Aug 19 08:31:40 2019 -0400

    Added Travis build info

commit dd23028125b5202bf1217944cfbacaaccb0d9f3a
Author: Larry Smith Jr <mrlesmithjr@gmail.com>
Date:   Mon Aug 19 08:30:37 2019 -0400

    First commit of Molecule testing

commit 0d3ea15257fa42a7e622fa1dd48b398164e78fc4
Author: Larry Smith Jr <mrlesmithjr@gmail.com>
Date:   Fri Apr 5 00:41:00 2019 -0400

    Create LICENSE

commit 8eb97d0c4ee771ffa8894dfcd7d06cbf3f89eb95
Author: Larry Smith Jr <mrlesmithjr@gmail.com>
Date:   Tue Mar 19 15:11:18 2019 -0400

    Updated repo info

commit 9913d597c363e340390abb9a7a1f98a2963033a5
Author: Larry Smith Jr <mrlesmithjr@gmail.com>
Date:   Tue Mar 19 15:09:10 2019 -0400

    Added .vscode settings

commit d028258b9173f1d526f79ab21a9e38789447f79a
Author: Larry Smith Jr <mrlesmithjr@gmail.com>
Date:   Tue Mar 19 15:07:53 2019 -0400

    First commit
