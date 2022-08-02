#include <iostream>
#include <vector>
#ifndef SLOT_HPP
#define SLOT_HPP 
/*

* func: 槽函数基类
* parm:
* return:
*/
template<class T>
class SlotBase
{
public:
    virtual void Exec(T param1) = 0;  //纯虚函数
    virtual ~SlotBase(){}
};
 
 
/*
* func: 槽函数
* parm:
* return:
*/
template<class T, class T1>
class Slot : public SlotBase<T1>
{
public:
 
    /* 定义Slot的时候，获取槽函数信息 */
    Slot(T* pObj, void (T::*func)(T1))
    {
        m_pSlotBase = pObj;
        m_Func = func;
    }
    /* signal触发时，调用 */
    void Exec(T1 param1)
    {
        (m_pSlotBase->*m_Func)(param1);
    }
 
private:
    /* 槽函数信息 暂存 */
    T* m_pSlotBase = NULL;
    void (T::*m_Func)(T1);
};
 
/*
* func: 信号
* parm:
* return:
*/
template<class T1>
class Signal
{
private:
    bool isBBind;
    SlotBase<T1>* m_pSlotSet; //这一句很重要，靠基类的指针来存储 信号槽指针
public:
    Signal():isBBind(false){}
    /* 模板函数 -> Bind时获取槽函数指针 */
    template<class T>
    void Bind(T* pObj, void(T::*func)(T1))
    {
        m_pSlotSet=new Slot<T,T1>(pObj,func);
        isBBind=true;
    }
    bool isBind(){return isBBind;}
    /* 重载操作符 -> signal触发机制 */
    void operator()(T1 param1)
    {
        m_pSlotSet->Exec(param1);
    }   
    ~Signal()
    {
        delete m_pSlotSet;
    }
};
#endif