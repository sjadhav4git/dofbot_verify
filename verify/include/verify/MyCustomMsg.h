// Generated by gencpp from file verify/MyCustomMsg.msg
// DO NOT EDIT!


#ifndef VERIFY_MESSAGE_MYCUSTOMMSG_H
#define VERIFY_MESSAGE_MYCUSTOMMSG_H


#include <string>
#include <vector>
#include <memory>

#include <ros/types.h>
#include <ros/serialization.h>
#include <ros/builtin_message_traits.h>
#include <ros/message_operations.h>

#include <std_msgs/Float64MultiArray.h>
#include <std_msgs/Float64MultiArray.h>
#include <std_msgs/Float64MultiArray.h>
#include <std_msgs/Float64MultiArray.h>
#include <std_msgs/Float64MultiArray.h>

namespace verify
{
template <class ContainerAllocator>
struct MyCustomMsg_
{
  typedef MyCustomMsg_<ContainerAllocator> Type;

  MyCustomMsg_()
    : joint_vars()
    , j1()
    , j2()
    , j3()
    , j4()  {
    }
  MyCustomMsg_(const ContainerAllocator& _alloc)
    : joint_vars(_alloc)
    , j1(_alloc)
    , j2(_alloc)
    , j3(_alloc)
    , j4(_alloc)  {
  (void)_alloc;
    }



   typedef  ::std_msgs::Float64MultiArray_<ContainerAllocator>  _joint_vars_type;
  _joint_vars_type joint_vars;

   typedef  ::std_msgs::Float64MultiArray_<ContainerAllocator>  _j1_type;
  _j1_type j1;

   typedef  ::std_msgs::Float64MultiArray_<ContainerAllocator>  _j2_type;
  _j2_type j2;

   typedef  ::std_msgs::Float64MultiArray_<ContainerAllocator>  _j3_type;
  _j3_type j3;

   typedef  ::std_msgs::Float64MultiArray_<ContainerAllocator>  _j4_type;
  _j4_type j4;





  typedef boost::shared_ptr< ::verify::MyCustomMsg_<ContainerAllocator> > Ptr;
  typedef boost::shared_ptr< ::verify::MyCustomMsg_<ContainerAllocator> const> ConstPtr;

}; // struct MyCustomMsg_

typedef ::verify::MyCustomMsg_<std::allocator<void> > MyCustomMsg;

typedef boost::shared_ptr< ::verify::MyCustomMsg > MyCustomMsgPtr;
typedef boost::shared_ptr< ::verify::MyCustomMsg const> MyCustomMsgConstPtr;

// constants requiring out of line definition



template<typename ContainerAllocator>
std::ostream& operator<<(std::ostream& s, const ::verify::MyCustomMsg_<ContainerAllocator> & v)
{
ros::message_operations::Printer< ::verify::MyCustomMsg_<ContainerAllocator> >::stream(s, "", v);
return s;
}


template<typename ContainerAllocator1, typename ContainerAllocator2>
bool operator==(const ::verify::MyCustomMsg_<ContainerAllocator1> & lhs, const ::verify::MyCustomMsg_<ContainerAllocator2> & rhs)
{
  return lhs.joint_vars == rhs.joint_vars &&
    lhs.j1 == rhs.j1 &&
    lhs.j2 == rhs.j2 &&
    lhs.j3 == rhs.j3 &&
    lhs.j4 == rhs.j4;
}

template<typename ContainerAllocator1, typename ContainerAllocator2>
bool operator!=(const ::verify::MyCustomMsg_<ContainerAllocator1> & lhs, const ::verify::MyCustomMsg_<ContainerAllocator2> & rhs)
{
  return !(lhs == rhs);
}


} // namespace verify

namespace ros
{
namespace message_traits
{





template <class ContainerAllocator>
struct IsFixedSize< ::verify::MyCustomMsg_<ContainerAllocator> >
  : FalseType
  { };

template <class ContainerAllocator>
struct IsFixedSize< ::verify::MyCustomMsg_<ContainerAllocator> const>
  : FalseType
  { };

template <class ContainerAllocator>
struct IsMessage< ::verify::MyCustomMsg_<ContainerAllocator> >
  : TrueType
  { };

template <class ContainerAllocator>
struct IsMessage< ::verify::MyCustomMsg_<ContainerAllocator> const>
  : TrueType
  { };

template <class ContainerAllocator>
struct HasHeader< ::verify::MyCustomMsg_<ContainerAllocator> >
  : FalseType
  { };

template <class ContainerAllocator>
struct HasHeader< ::verify::MyCustomMsg_<ContainerAllocator> const>
  : FalseType
  { };


template<class ContainerAllocator>
struct MD5Sum< ::verify::MyCustomMsg_<ContainerAllocator> >
{
  static const char* value()
  {
    return "25454e64d6a7089f1c508394e699d763";
  }

  static const char* value(const ::verify::MyCustomMsg_<ContainerAllocator>&) { return value(); }
  static const uint64_t static_value1 = 0x25454e64d6a7089fULL;
  static const uint64_t static_value2 = 0x1c508394e699d763ULL;
};

template<class ContainerAllocator>
struct DataType< ::verify::MyCustomMsg_<ContainerAllocator> >
{
  static const char* value()
  {
    return "verify/MyCustomMsg";
  }

  static const char* value(const ::verify::MyCustomMsg_<ContainerAllocator>&) { return value(); }
};

template<class ContainerAllocator>
struct Definition< ::verify::MyCustomMsg_<ContainerAllocator> >
{
  static const char* value()
  {
    return "# MyCustomMsg.msg\n"
"\n"
"std_msgs/Float64MultiArray joint_vars\n"
"std_msgs/Float64MultiArray j1\n"
"std_msgs/Float64MultiArray j2\n"
"std_msgs/Float64MultiArray j3\n"
"std_msgs/Float64MultiArray j4\n"
"\n"
"================================================================================\n"
"MSG: std_msgs/Float64MultiArray\n"
"# Please look at the MultiArrayLayout message definition for\n"
"# documentation on all multiarrays.\n"
"\n"
"MultiArrayLayout  layout        # specification of data layout\n"
"float64[]         data          # array of data\n"
"\n"
"\n"
"================================================================================\n"
"MSG: std_msgs/MultiArrayLayout\n"
"# The multiarray declares a generic multi-dimensional array of a\n"
"# particular data type.  Dimensions are ordered from outer most\n"
"# to inner most.\n"
"\n"
"MultiArrayDimension[] dim # Array of dimension properties\n"
"uint32 data_offset        # padding elements at front of data\n"
"\n"
"# Accessors should ALWAYS be written in terms of dimension stride\n"
"# and specified outer-most dimension first.\n"
"# \n"
"# multiarray(i,j,k) = data[data_offset + dim_stride[1]*i + dim_stride[2]*j + k]\n"
"#\n"
"# A standard, 3-channel 640x480 image with interleaved color channels\n"
"# would be specified as:\n"
"#\n"
"# dim[0].label  = \"height\"\n"
"# dim[0].size   = 480\n"
"# dim[0].stride = 3*640*480 = 921600  (note dim[0] stride is just size of image)\n"
"# dim[1].label  = \"width\"\n"
"# dim[1].size   = 640\n"
"# dim[1].stride = 3*640 = 1920\n"
"# dim[2].label  = \"channel\"\n"
"# dim[2].size   = 3\n"
"# dim[2].stride = 3\n"
"#\n"
"# multiarray(i,j,k) refers to the ith row, jth column, and kth channel.\n"
"\n"
"================================================================================\n"
"MSG: std_msgs/MultiArrayDimension\n"
"string label   # label of given dimension\n"
"uint32 size    # size of given dimension (in type units)\n"
"uint32 stride  # stride of given dimension\n"
;
  }

  static const char* value(const ::verify::MyCustomMsg_<ContainerAllocator>&) { return value(); }
};

} // namespace message_traits
} // namespace ros

namespace ros
{
namespace serialization
{

  template<class ContainerAllocator> struct Serializer< ::verify::MyCustomMsg_<ContainerAllocator> >
  {
    template<typename Stream, typename T> inline static void allInOne(Stream& stream, T m)
    {
      stream.next(m.joint_vars);
      stream.next(m.j1);
      stream.next(m.j2);
      stream.next(m.j3);
      stream.next(m.j4);
    }

    ROS_DECLARE_ALLINONE_SERIALIZER
  }; // struct MyCustomMsg_

} // namespace serialization
} // namespace ros

namespace ros
{
namespace message_operations
{

template<class ContainerAllocator>
struct Printer< ::verify::MyCustomMsg_<ContainerAllocator> >
{
  template<typename Stream> static void stream(Stream& s, const std::string& indent, const ::verify::MyCustomMsg_<ContainerAllocator>& v)
  {
    s << indent << "joint_vars: ";
    s << std::endl;
    Printer< ::std_msgs::Float64MultiArray_<ContainerAllocator> >::stream(s, indent + "  ", v.joint_vars);
    s << indent << "j1: ";
    s << std::endl;
    Printer< ::std_msgs::Float64MultiArray_<ContainerAllocator> >::stream(s, indent + "  ", v.j1);
    s << indent << "j2: ";
    s << std::endl;
    Printer< ::std_msgs::Float64MultiArray_<ContainerAllocator> >::stream(s, indent + "  ", v.j2);
    s << indent << "j3: ";
    s << std::endl;
    Printer< ::std_msgs::Float64MultiArray_<ContainerAllocator> >::stream(s, indent + "  ", v.j3);
    s << indent << "j4: ";
    s << std::endl;
    Printer< ::std_msgs::Float64MultiArray_<ContainerAllocator> >::stream(s, indent + "  ", v.j4);
  }
};

} // namespace message_operations
} // namespace ros

#endif // VERIFY_MESSAGE_MYCUSTOMMSG_H
