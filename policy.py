from z3 import *
from id_match import iam_pattern_to_regex
from iam import *

policies = [{
    "PolicyVersion": {
        "Document": {
            "Version": "2012-10-17",
            "Statement": [

                {
                    "Sid": "VisualEditor1",
                    "Effect": "Allow",
                    "Action": "sts:*",
                    "Resource": "arn:aws:iam::218925562655:role/testrole*"
                }
            ]
        },
        "VersionId": "v1",
        "IsDefaultVersion": True,
        "CreateDate": "2022-11-21T06:45:18+00:00"
    }
},{
    "PolicyVersion": {
        "Document": {
            "Version": "2012-10-17",
            "Statement": [
                {
                    "Effect": "Allow",
                    "Action": "s3:*",
                    "Resource": "*"
                }
            ]
        },
        "VersionId": "v1",
        "IsDefaultVersion": False,
        "CreateDate": "2015-02-06T18:40:58+00:00"
    }
}]


"""
Or(And(u == StringVal("arn:aws:iam::218925562655:user/test1"), 
                InRe(a, iam_pattern_to_regex("sts:*")),
                InRe(r, iam_pattern_to_regex("arn:aws:iam::218925562655:role/testrole*")),
                e == BoolVal(True)),

                And(u == StringVal("arn:aws:iam::218925562655:role/testrole1"), 
                    InRe(a, iam_pattern_to_regex("sts:*")),
                    InRe(r, iam_pattern_to_regex("arn:aws:iam::218925562655:role/testrole*")),
                    e == BoolVal(True)),

               And(u == StringVal("arn:aws:iam::218925562655:role/testrole2"),
                    InRe(a, iam_pattern_to_regex("s3:*")),
                    InRe(r, iam_pattern_to_regex("*")))
    )


"""

flat_map = lambda f, xs: (y for ys in xs for y in f(ys))

def extract(policy):
    return policy["PolicyVersion"]["Document"]["Statement"]

print(list(flat_map(extract,policies)))

def constructInRe(n):
    return lambda x: InRe(x, iam_pattern_to_regex(n))

def constructEquality(n):
    return lambda x: x == n

def constructAnd(*args):
    return And(args)

def constructOr(*args):
    return Or(args)

def constructListCheck(check,ls):
    return tuple(map(check,ls))

def generatePolicyContraints(user,policy):
    effect = policy["Effect"] == "Allow"
    actions = policy["Action"]
    resources = policy["Resource"]

    actions = actions if isinstance(actions,list) else [actions]
    resources = resources if isinstance(resources,list) else [resources]

    return (
        constructEquality(BoolVal(effect)),
        constructEquality(StringVal(user)),
        constructListCheck(constructInRe,actions),
        constructListCheck(constructInRe,resources))

def usePolicyContraints(e, u, a, r, ls):
    
    def openParams(l):
        x1,x2,x3,x4 = l
        return And(x1(e),x2(u),Or(tuple(map(lambda x : x(a),x3))),Or(tuple(map(lambda x : x(r),x4))))

    return Or(list(map(openParams,ls)))

def usePolcies(ls):
    return usePolicyContraints(BoolVal(True),StringVal("arn:aws:iam::218925562655:user/test1"),StringVal("*"),StringVal("*"),list(map(lambda x: generatePolicyContraints(*x),ls)))

print(usePolcies(transformPolicyArray(get_all_identities_with_policies())))
# print(usePolicyContraints(BoolVal(True),StringVal("arn:aws:iam::218925562655:user/test1"),StringVal("*"),StringVal("*"),list(map(lambda x: generatePolicyContraints(*x),zip(flat_map(extract,policies),["arn:aws:iam::218925562655:user/test1"]* len(policies))))))
 
 
    # match actions:
    #     case [*action]:
    #         for a in action:
    #             pass
    #     case *action:
    #         pass
    
    # match resources:
    #     case [*resource]:
    #         for r in resource:
    #             pass
    #     case *resource:
    #         pass
    




def Policy(e, u, a, r):
    return Or(
        And(
        e == BoolVal(True),
        u == StringVal("arn:aws:iam::218925562655:user/test1"), 
        InRe(a, iam_pattern_to_regex("sts:*")),
        InRe(r, iam_pattern_to_regex("arn:aws:iam::218925562655:role/testrole*"))),
                


        And(e == BoolVal(True),
            u == StringVal("arn:aws:iam::218925562655:user/test1"),
                InRe(a, iam_pattern_to_regex("s3:*")),
                InRe(r, iam_pattern_to_regex("*"))))


# print(Policy(BoolVal(True),StringVal("arn:aws:iam::218925562655:user/test1"),StringVal("*"),StringVal("*")))
# print(list(map(lambda x: mapIdentityToPolicies(*x),get_all_identities_with_policies())))
prove(Policy(BoolVal(True),StringVal("arn:aws:iam::218925562655:user/test1"),StringVal("*"),StringVal("*")) == usePolicyContraints(BoolVal(True),StringVal("arn:aws:iam::218925562655:user/test1"),StringVal("*"),StringVal("*"),list(map(lambda x: generatePolicyContraints(*x),zip(["arn:aws:iam::218925562655:user/test1"] * len(policies),flat_map(extract,policies))))))
                # And(u == StringVal("arn:aws:iam::218925562655:role/testrole1"), 
                #     InRe(a, iam_pattern_to_regex("sts:*")),
                #     InRe(r, iam_pattern_to_regex("arn:aws:iam::218925562655:role/testrole*")),
                #     e == BoolVal(True)),


                #                 {
                #     "Sid": "VisualEditor0",
                #     "Effect": "Allow",
                #     "Action": [
                #         "sts:GetSessionToken",
                #         "sts:DecodeAuthorizationMessage",
                #         "sts:GetAccessKeyInfo",
                #         "sts:GetCallerIdentity",
                #         "sts:GetServiceBearerToken"
                #     ],
                #     "Resource": "*"
                # },