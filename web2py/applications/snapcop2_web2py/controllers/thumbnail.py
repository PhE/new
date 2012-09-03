import redis

def thumb():
    """
    Renvoie dans photos la liste des x dernières photos prises
  
    """
    # connexion redis
    # récupérer le nb de photo prises (GET frames)
    # récupérere la liste des chemins des photos (LRANGE -5 -1)

    cx=redis.Redis()
    frames = int(cx.get('frames'))
    frames = 3
    image=[]
    photos = cx.lrange('captures', -frames, -1)
    photos = [
      '/snapcop2_web2py/static/images/css3buttons_backgrounds.png', 
      '/snapcop2_web2py/static/images/poweredby.png', 
      '/snapcop2_web2py/static/images/css3buttons_backgrounds.png', 
      '/snapcop2_web2py/static/images/ui-icons_222222_256x240.png', 
    ]

    ''' INUTILE !!!
    for i in range(0, frames):
        photo = serie[i]
        image+=[
        A(IMG(_src=URL('static/Photos', 'thumb%s'%photo[-18:]), _alt="Capt"),
                  _href=URL('static/Photos', photo[-22:])),
              ]
    stack = cx.get('Stack')
    image2=[
        A(IMG(_src=URL('static/Photos', 'thumb%s'%stack), _alt="Capt"),
                  _href=URL('static/Photos', stack)),
              ]
    #return dict(Photos=image, Stacking=image2)
    '''    
    auteur = 'Eric DURAND'
    return locals()
    
    
