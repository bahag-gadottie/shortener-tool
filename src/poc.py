# -*- coding: utf-8 -*-
import pandas as pd
from app.infra.misc import query_pgsql
from app.core.misc import sanitize, tokenize, replace, wrap, token_sort_ratio
import random
import math

products_poc = """
        '4037756002008',
        '4037756002053',
        '4037756032005',
        '4037756032012',
        '4037756032029',
        '4037756032036',
        '4037756032043',
        '4037756032050',
        '4037756032067',
        '4037756032074',
        '4037756054809',
        '4037756054816',
        '4037756054823',
        '4037756054830',
        '4037756054847',
        '4037756060435',
        '4037756108106',
        '4037756108113',
        '4037756108120',
        '4037756108137',
        '4037756108144',
        '4037756108038',
        '4037756104283',
        '4037756506223',
        '4037756001506',
        '4037756001513',
        '4037756001520',
        '4037756001537',
        '4037756001902',
        '4037756001919',
        '4037756001926',
        '4037756001933',
        '4037756001940',
        '4037756001957',
        '4037756001551',
        '4037756001568',
        '4037756001575',
        '4037756001582'
"""
df_products = pd.DataFrame(query_pgsql(f"""
    select ean, product_description from shc_tool_products where ean in (
        '9999999999999', {products_poc}
    ) order by product_description
    """, 'postgres'))

df_definitions = dict(query_pgsql('select shc_description as to_replace, '
                                  'shc_name as replacement from shc_tool_definitions '
                                  'order by length(shc_description) desc, length(shc_name) desc', 'postgres'))

df_products.rename(columns={0: 'ean', 1: 'description'}, inplace=True)

df = df_products.copy()
del df_products

df['sanitised'] = df['description'].apply(lambda f: sanitize(f)[0])
df['shortened'] = df['sanitised'].apply(lambda w: replace(w, df_definitions))

# approaches
df['tokenized'] = df['shortened'].apply(lambda l: tokenize(l))
df['sort_ratio_tokenized'] = df.apply(lambda l: token_sort_ratio(l['tokenized'], l['shortened']), axis=1)
df['wrapped'] = df['shortened'].apply(lambda l: wrap(l))
df['sort_ratio_wrapped'] = df.apply(lambda l: token_sort_ratio(l['wrapped'], l['shortened']), axis=1)

# other demo with different wrap
df['tokenized_2'] = df['shortened'].apply(lambda l: tokenize(l, n_lines=2))
df['sort_ratio_tokenized_2'] = df.apply(lambda l: token_sort_ratio(l['tokenized'], l['shortened']), axis=1)
df['wrapped_2'] = df['shortened'].apply(lambda l: wrap(l, n_lines=2))
df['sort_ratio_wrapped_2'] = df.apply(lambda l: token_sort_ratio(l['wrapped'], l['shortened']), axis=1)

del df['ean'], df['description']

df.to_csv(f'/Users/gadotte/PoC_abbreviations_id{math.ceil(random.random()  * 100000)}.csv',
          sep=';', encoding='utf8')

print('\n...end of PoC!')
