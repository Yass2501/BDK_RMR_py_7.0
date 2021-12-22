import matplotlib.pyplot as plt
import datetime

d0 = datetime.date(2021,11,10)
period = 3
nPeriod = 15
p =  []
pint = []
X = []
name = []
for i in range(0,nPeriod):
    tmp = [d0,d0 + datetime.timedelta(days=period)]
    tmpint = tmp[0].strftime('%d-%m') + ' to ' + tmp[1].strftime('%d-%m')
    p.append(tmp)
    pint.append(tmpint)
    X.append(i*i-i)
    d0 = d0 + datetime.timedelta(days=period)
    name.append('Period '+str(i))

print(pint)

plt.bar(name,X)
plt.xticks(rotation='vertical')
plt.xticks(rotation=45, ha='right')
#plt.xticks(rotation=30, ha='right')
plt.ylim(0, max(X))
plt.show()
