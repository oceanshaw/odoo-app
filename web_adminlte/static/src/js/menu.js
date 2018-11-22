odoo.define('web.AdminLTEMenu', function (require) {
    var Menu = require('web.Menu');
    var session = require('web.session');

    Menu.include({
        init: function() {
            var self = this;
            this._super.apply(this, arguments);
            this.on("menu_bound", this, function() {
                // launch the fetch of needaction counters, asynchronous
                var $all_menus = self.$el.parents('.main-sidebar').find('.sidebar').find('[data-menu]');
                var all_menu_ids = _.map($all_menus, function (menu) {return parseInt($(menu).attr('data-menu'), 10);});
                if (!_.isEmpty(all_menu_ids)) {
                    this.do_load_needaction(all_menu_ids);
                }
            });
        },
        open_menu: function(id) {
            this.current_menu = id;
            session.active_id = id;
            var $clicked_menu, $sub_menu, $main_menu;
            $clicked_menu = this.$el.add(this.$secondary_menus).find('a[data-menu=' + id + ']');
            this.trigger('open_menu', id, $clicked_menu);

            if (this.$secondary_menus.has($clicked_menu).length) {
                $sub_menu = $clicked_menu.parents('.oe_secondary_menu');
                $main_menu = this.$el.find('a[data-menu=' + $sub_menu.data('menu-parent') + ']');
            } else {
                $sub_menu = this.$secondary_menus.find('.oe_secondary_menu[data-menu-parent=' + $clicked_menu.attr('data-menu') + ']');
                $main_menu = $clicked_menu;
            }

            // Activate current main menu
            // this.$el.find('.active').removeClass('active');
            // $main_menu.parent().addClass('active');

            // Show current sub menu
            this.$secondary_menus.find('.oe_secondary_menu').hide();
            $sub_menu.show();

            // Hide/Show the leftbar menu depending of the presence of sub-items
            this.$secondary_menus.toggleClass('o_hidden', !$sub_menu.children().length);

            // Activate current menu item and show parents
            this.$secondary_menus.find('.active').removeClass('active');
            if ($main_menu !== $clicked_menu) {
                $clicked_menu.parents().removeClass('o_hidden');
                if ($clicked_menu.is('.oe_menu_toggler')) {
                    $clicked_menu.toggleClass('oe_menu_opened').siblings('.oe_secondary_submenu:first').toggleClass('o_hidden');
                } else {
                    $clicked_menu.parent().addClass('active');
                }
            }
            // add a tooltip to cropped menu items
            this.$secondary_menus.find('.oe_secondary_submenu li a span').each(function() {
                $(this).tooltip(this.scrollWidth > this.clientWidth ? {title: $(this).text().trim(), placement: 'right'} :'destroy');
           });

            var $clicked_menu_parent = $clicked_menu.parent();
            $('.sidebar-menu').find('li').removeClass('active');
            var parents = $clicked_menu.parentsUntil('.oe_application_menu_placeholder');
            for(var i=0, l=parents.length; i < l; i++){
                var parent = parents[i];
                if(parent.tagName === 'LI'){
                    $(parent).addClass('active')
                }
            }
        },
        menu_click: function(id, needaction) {
                if (!id) { return; }

                // find back the menuitem in dom to get the action
                var $item = this.$el.find('a[data-menu=' + id + ']');
                if (!$item.length) {
                    $item = this.$secondary_menus.find('a[data-menu=' + id + ']');
                }
                var action_id = $item.data('action-id');
                // If first level menu doesnt have action trigger first leaf
                if (!action_id) {
                    if(this.$el.has($item).length) {
                        var $sub_menu = $item.find('+ul');
                        var $items = $sub_menu.find('a[data-action-id]').filter('[data-action-id!=""]');
                        if($items.length) {
                            action_id = $items.data('action-id');
                            id = $items.data('menu');
                        }
                    }
                }
                if (action_id) {
                    this.trigger('menu_click', {
                        action_id: action_id,
                        needaction: needaction,
                        id: id,
                        previous_menu_id: this.current_menu // Here we don't know if action will fail (in which case we have to revert menu)
                    }, $item);
                } else {
                    console.log('Menu no action found web test 04 will fail');
                }
                this.open_menu(id);
            },
    })
});