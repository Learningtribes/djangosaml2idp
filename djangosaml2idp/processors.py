import logging
from django_countries.fields import Country

logger = logging.getLogger(__name__)

class BaseProcessor(object):
  """
    Processor class is used to determine if a user has access to a client service of this IDP
    and to create the identity dictionary sent to the SP
  """

  def has_access(self, user):
    return True

  def create_identity(self, user, sp_mapping):
    identity = {}
    for out_attr, user_attr in sp_mapping.items():
        if hasattr(user, user_attr):
            identity[out_attr] = getattr(user, user_attr)
        else:
            if hasattr(user, "profile"):
                profile = getattr(user, "profile")
                if hasattr(profile, user_attr):
                    val = getattr(profile, user_attr)
                    if type(val) == Country:
                        val = "%s" % val
                    identity[out_attr] = val
    # logger.info("identity = %s" % identity)
    return identity
