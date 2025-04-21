creqit.provide('creqit.meta');

creqit.meta.MetaCampaign = class MetaCampaign extends creqit.ui.form.Controller {
    setup() {
        this.setup_queries();
    }

    setup_queries() {
        this.frm.set_query('campaign', () => {
            return {
                filters: {
                    'status': 'ACTIVE'
                }
            };
        });
    }
};

extend_cscript(cur_frm.cscript, new creqit.meta.MetaCampaign({frm: cur_frm})); 