window.onload = function() {
	CKEDITOR.on('instanceCreated', function(event) {
		var editor = event.editor, element = editor.element;

		if (element.is('h1', 'h2', 'h3') || element.getAttribute('id') == 'taglist') {
			editor.on('configLoaded', function() {

				editor.config.removePlugins = 'colorbutton,find,flash,font,' + 'forms,iframe,image,newpage,removeformat,' + 'smiley,specialchar,stylescombo,templates';

				editor.config.toolbarGroups = [{
					name : 'editing',
					groups : ['basicstyles', 'links']
				}, {
					name : 'undo'
				}, {
					name : 'clipboard',
					groups : ['selection', 'clipboard']
				}, {
					name : 'about'
				}];
			});
		}
	})
};
