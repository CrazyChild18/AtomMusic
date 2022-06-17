var link = $('.com__nav-link');
var linkParent = link.parent('li');
var section = $('.com__section');
var sectionContent = section.find('*');

var switchTab = function() {
	var p = $(this).parent('li');
	var i  = p.index();
	var s = section.eq(i);
	var c = s.find('*');

	section.removeClass('active');
	sectionContent.removeAttr('style');
	s.addClass('active');

	c.css({
		transform: 'none',
		opacity: 1
	});

	linkParent.removeClass('active');
	p.addClass('active');

	return false;
};

link.on('click', switchTab);

function activeFirst() {
	section.first().addClass('active');
	section.first().find('*').css({
		transform: 'none',
		opacity: 1
	});
	linkParent.first().addClass('active');
}

activeFirst();