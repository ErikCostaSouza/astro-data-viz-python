from astroquery.mast import Observations
obs_table = Observations.query_object('M51', radius=0.1)
if len(obs_table)==0:
    print('no obs')
else:
    hubble_obs = obs_table[obs_table['obs_collection']=='HST'] if 'obs_collection' in obs_table.colnames else obs_table
    for obs in hubble_obs[:10]:
        products = Observations.get_product_list(obs)
        col = None
        for c in products.colnames:
            if 'file' in c.lower() or 'name' in c.lower() or 'filename' in c.lower():
                col = c; break
        nfits = 0
        if col:
            nfits = sum(1 for p in products if str(p[col]).lower().endswith('.fits'))
        instr = obs['instrument_name'] if 'instrument_name' in obs.colnames else ''
        print(obs['obs_id'], instr, 'fits=', nfits)
