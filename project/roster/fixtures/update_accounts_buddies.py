import yaml
from itertools import count

data =  yaml.load(open('roster.yaml','r'))
buddies =  filter(lambda o: o.get('model')== 'roster.buddy',data)

seq = count(7)

def buddy2account(buddy):
    fields = buddy.get('fields')
    nick = '@'+fields.get('nickname')[:9]
    name = 'Payments from '+' '.join(filter(None, map(fields.get, ('first_name', 'middle_name', 'surname',))))
    return dict(
        fields=dict(
            name=name,
            currency=1,
            type=4, # credit
            symbol=nick,
        ),
        model= 'roster.logicaccount',
        pk= seq.next(),
    )

accounts = map(buddy2account, buddies)
yaml.dump(accounts, open('account.yaml', 'w'))

def buddy_update(buddy):
    fields = dict()
    fields.update(buddy.get('fields'))
    acc, = filter(lambda a: a.get('fields').get('symbol')=='@'+fields.get('nickname')[:9], accounts )
    fields.update(
        logic_account = acc.get('pk'),
    )
    return dict(
        model = buddy.get('model'),
        pk = buddy.get('pk'),
        fields = fields,
    )
buddies = map(buddy_update, buddies)
yaml.dump(buddies, open('buddy.yaml', 'w'))
